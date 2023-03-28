import asyncio
import re
#import json
import logging
import random
import datetime
from typing import Dict, List

from pyonvifsrv.context import Context
from pyonvifsrv.service_base import ServiceBase
from pyonvifsrv.utils import parseSOAPString, getServiceNameFromOnvifNS, getMethodNameFromBody, decapitalize, envelopeHeader, envelopeFooter, errorReponse
from pyonvifsrv.const import ERROR_TYPE

logger = logging.getLogger(__name__)

def getDurationAsSeconds(duration):
    regex = re.compile(r'^P((\d+Y)?(\d+M)?(\d+D)?)?(T(\d+H)?(\d+M)?(\d+S)?)?$')
    match = re.match(regex, duration)
    if not match:
        raise Exception('Invalid duration string: {}'.format(duration))

    # Debugging
    # for i in range(1, len(match.groups())+1):
    #     print('group {}: {}'.format(i, match.group(i)))

    # The match groups contain the characters (Y, M, D, H, M, S) at the end
    # We remove them with [:-1]
    # match.group(5) is not used, because it matches the whole T part, e.g. PT60S gives T60S
    years = int(match.group(2)[:-1]) if match.group(2) else 0
    months = int(match.group(3)[:-1]) if match.group(3) else 0
    days = int(match.group(4)[:-1]) if match.group(4) else 0
    hours = int(match.group(6)[:-1]) if match.group(6) else 0
    minutes = int(match.group(7)[:-1]) if match.group(7) else 0
    seconds = int(match.group(8)[:-1]) if match.group(8) else 0
   
    return (years * 365 * 24 * 60 * 60) + (months * 30 * 24 * 60 * 60) + (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds

class Message:
    def __init__(self, topicname: str, payload: any):
        self.topicname = topicname
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)
        self.payload = payload
        self.properyOperation = 'Changed'

    def toXml(self) -> str:
        return '''
            <wsnt:NotificationMessage>
                <wsnt:Topic Dialect="http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet">{topicname}</wsnt:Topic>
                <wsnt:Message>
                    <tt:Message xmlns:tt="http://www.onvif.org/ver10/schema" UtcTime="{timestamp}" PropertyOperation="{properyOperation}">
                        <tt:Source>
                            <tt:SimpleItem Name="Source" Value="{sourceValue}" />
                        </tt:Source>
                        <tt:Data>
                            <tt:SimpleItem Name="State" Value="{stateValue}" />
                        </tt:Data>
                    </tt:Message>
                </wsnt:Message>
            </wsnt:NotificationMessage>
        '''.format(topicname=self.topicname,
                   timestamp=self.timestamp.isoformat(sep="T", timespec="seconds").replace("+00:00", "Z"),
                   sourceValue=self.payload["source_value"],
                   stateValue=self.payload["state_value"],
                   properyOperation=self.properyOperation)

class PullPointSubscription():
    def __init__(self, id: str, expirationTime: datetime):
        self.id = id
        self.expirationTime: datetime = expirationTime
        self.messages: List[Message] = []
        self.future = asyncio.get_running_loop().create_future()

    def addMessage(self, message: Message):
        self.messages.append(message)
        if not self.future.done:
            self.future.set_result(True)

    async def reNew(self, expirationTime: datetime):
        self.expirationTime = expirationTime
        self.future.cancel()
        try:
            await self.future
        except asyncio.CancelledError:
            pass
        self.future = asyncio.get_running_loop().create_future()

    async def wait_for(self, timeoutInSeconds: int):
        try:
            await asyncio.wait_for(self.future, timeoutInSeconds)
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass

class EventsService(ServiceBase):
    serviceName = "events"
    pullPointPath = r"/onvif/pullpoint"

    def __init__(self, context: Context):
        super().__init__(context)

        self.subscriptions: Dict[str, PullPointSubscription]= {}

    def triggerEvent(self, topicname: str, payload: any):
        for subscription in self.subscriptions.values():
            subscription.addMessage(Message(topicname, payload))

    def getRequestHandler(self):
        handlers = ServiceBase.getRequestHandler(self)
        handlers += [((self.pullPointPath + r"/(\d+)", self._SubscriptionHandler, dict(serviceInstance=self)))]
        return handlers

    class _SubscriptionHandler(ServiceBase._ServiceHandler):

        async def post(self, subscriptionId):
            reqBody = self.request.body.decode('utf-8')
            #logger.debug(f"HTTP request body: {reqBody}")

            # Parse the SOAP XML and create a dictionary which contains the
            # SOAP header and body
            reqData = parseSOAPString(reqBody)
            reqData["urlParams"] = {"subscriptionId": subscriptionId}
            #logging.debug(f"data: \n{json.dumps(reqData, indent=4)}")

            [responseCode, response] = await self.callMethodFromSoapRequestData(reqData)
            self.set_status(responseCode)
            self.write(response)
            self.finish()

    def createPullPointSubscription(self, data):

        subscriptionId = str(random.randint(0, 2**32 - 1))

        initialTerminationTime: str = data["body"]["CreatePullPointSubscription"]["InitialTerminationTime"]
        expireInSeconds = getDurationAsSeconds(initialTerminationTime)
        logger.debug("New PullPointSubscription {subscriptionId} expires in {expireInSeconds} seconds".format(subscriptionId=subscriptionId, expireInSeconds=expireInSeconds))

        currentTime: datetime = datetime.datetime.now(datetime.timezone.utc)
        expirationTime: datetime = currentTime + datetime.timedelta(seconds=expireInSeconds)

        subscription = PullPointSubscription(subscriptionId, expirationTime)

        self.subscriptions[subscriptionId] = subscription

        return '''
            <tev:CreatePullPointSubscriptionResponse>
                <tev:SubscriptionReference>
                    <wsa5:Address>{pullPointAddress}</wsa5:Address>
                </tev:SubscriptionReference>
                <wsnt:CurrentTime>{currentTime}</wsnt:CurrentTime>
                <wsnt:TerminationTime>{expirationTime}</wsnt:TerminationTime>
            </tev:CreatePullPointSubscriptionResponse>		
        '''.format(pullPointAddress=self.context.hostUrl + self.pullPointPath + "/" + subscriptionId,
                   currentTime=currentTime.isoformat(sep="T", timespec="seconds").replace("+00:00", "Z"),
                   expirationTime=expirationTime.isoformat(sep="T", timespec="seconds")).replace("+00:00", "Z")

    async def pullMessages(self, data):
        subscriptionId = data["urlParams"]["subscriptionId"]
        if subscriptionId not in self.subscriptions:
            return errorReponse(ERROR_TYPE.INVALID_ARGS_VAL, "Subscription not found: " + subscriptionId)

        subscription = self.subscriptions[subscriptionId]

        messagesXml = ''
        for message in subscription.messages:
            messagesXml += message.toXml()

        # Remove all messages from the subscription
        subscription.messages = []

        currentTime: datetime = datetime.datetime.now(datetime.timezone.utc)
        terminationTime: datetime = subscription.expirationTime

        timeoutInSeconds = getDurationAsSeconds(data["body"]["PullMessages"]["Timeout"])

        logger.debug("Waiting for event messages (PullPointSubscription {subscriptionId}): Timeout in {timeoutInSeconds} seconds".format(subscriptionId=subscriptionId, timeoutInSeconds=timeoutInSeconds))

        # sleep(timeoutInSeconds)
        #await asyncio.sleep(timeoutInSeconds)
        await subscription.wait_for(timeoutInSeconds)

        return '''
            <tev:PullMessagesResponse>
                <tev:CurrentTime>{currentTime}</tev:CurrentTime>
                <tev:TerminationTime>{terminationTime}</tev:TerminationTime>
                {messagesXml}
            </tev:PullMessagesResponse>
        '''.format(currentTime=currentTime.isoformat(sep="T", timespec="seconds").replace("+00:00", "Z"),
                   terminationTime=terminationTime.isoformat(sep="T", timespec="seconds").replace("+00:00", "Z"),
                   messagesXml=messagesXml)

    async def renew(self, data):
        subscriptionId = data["urlParams"]["subscriptionId"]
        if subscriptionId not in self.subscriptions:
            return errorReponse(ERROR_TYPE.INVALID_ARGS_VAL, "Subscription not found: " + subscriptionId)

        subscription = self.subscriptions[subscriptionId]

        terminationTimeInSeconds = getDurationAsSeconds(data["body"]["Renew"]["TerminationTime"])

        currentTime: datetime = datetime.datetime.now(datetime.timezone.utc)
        terminationTime: datetime = currentTime + datetime.timedelta(seconds=terminationTimeInSeconds)

        await subscription.reNew(terminationTime)

        logger.debug("Renew PullPointSubscription {subscriptionId}: new expirationTime: {terminationTime}"
                     .format(subscriptionId=subscriptionId,
                             terminationTime=terminationTime.isoformat(sep="T", timespec="seconds").replace("+00:00", "Z")))

        return '''
            <wsnt:RenewResponse>
                <wsnt:TerminationTime>{terminationTime}</wsnt:TerminationTime>
                <wsnt:CurrentTime>{currentTime}</wsnt:CurrentTime>
            </wsnt:RenewResponse>
        '''.format(terminationTime=terminationTime.isoformat(sep="T", timespec="seconds").replace("+00:00", "Z"),
                   currentTime=currentTime.isoformat(sep="T", timespec="seconds").replace("+00:00", "Z"))

    def unsubscribe(self, data):
        subscriptionId = data["urlParams"]["subscriptionId"]
        if subscriptionId in self.subscriptions:
            del self.subscriptions[subscriptionId]
            return '''
                <wsnt:UnsubscribeResponse></wsnt:UnsubscribeResponse>        
            '''
        else:
            return errorReponse(ERROR_TYPE.INVALID_ARGS_VAL, "Subscription not found: " + subscriptionId)

    def getEventProperties(self, data):
        return '''
            <tev:GetEventPropertiesResponse>
                <tev:TopicNamespaceLocation>http://www.onvif.org/onvif/ver10/topics/topicns.xml</tev:TopicNamespaceLocation>
                <wsnt:FixedTopicSet>true</wsnt:FixedTopicSet>
                <wstop:TopicSet>
                    <tns1:VideoSource wstop:topic="false">
                        <MotionAlarm wstop:topic="true">
                            <tt:MessageDescription IsProperty="true">
                                <tt:Source>
                                    <tt:SimpleItemDescription Name="Source"	Type="tt:ReferenceToken"/>
                                </tt:Source>
                                <tt:Data>
                                    <tt:SimpleItemDescription Name="State" Type="xsd:boolean"/>
                                </tt:Data>
                            </tt:MessageDescription>
                        </MotionAlarm>
                        <ImageTooDark wstop:topic="false">
                            <ImagingService wstop:topic="true">
                                <tt:MessageDescription IsProperty="true">
                                    <tt:Source>
                                        <tt:SimpleItemDescription Name="Source" Type="tt:ReferenceToken"/>
                                    </tt:Source>
                                    <tt:Data>
                                        <tt:SimpleItemDescription Name="State" Type="xsd:boolean"/>
                                    </tt:Data>
                                </tt:MessageDescription>
                            </ImagingService>
                        </ImageTooDark>
                    </tns1:VideoSource>
                    <tns1:Media wstop:topic="false">
                        <ProfileChanged wstop:topic="true">
                            <tt:MessageDescription IsProperty="false">
                                <tt:Data>
                                    <tt:SimpleItemDescription Name="Token" Type="tt:ReferenceToken"/>
                                </tt:Data>
                            </tt:MessageDescription>
                        </ProfileChanged>
                        <ConfigurationChanged wstop:topic="true">
                            <tt:MessageDescription IsProperty="false">
                                <tt:Source>
                                    <tt:SimpleItemDescription Name="Token" Type="tt:ReferenceToken"/>
                                </tt:Source>
                                <tt:Data>
                                    <tt:SimpleItemDescription Name="Type" Type="xsd:string"/>
                                </tt:Data>
                            </tt:MessageDescription>
                        </ConfigurationChanged>
                    </tns1:Media>
                    <tns1:RuleEngine wstop:topic="true">
                        <CellMotionDetector wstop:topic="true">
                            <Motion wstop:topic="true">
                                <tt:MessageDescription IsProperty="true">
                                    <tt:Source>
                                        <tt:SimpleItemDescription Name="VideoSourceConfigurationToken" Type="tt:ReferenceToken"/>
                                        <tt:SimpleItemDescription Name="VideoAnalyticsConfigurationToken" Type="tt:ReferenceToken"/>
                                        <tt:SimpleItemDescription Name="Rule" Type="xsd:string"/>
                                    </tt:Source>
                                    <tt:Data>
                                        <tt:SimpleItemDescription Name="IsMotion" Type="xsd:boolean"/>
                                    </tt:Data>
                                </tt:MessageDescription>
                            </Motion>
                        </CellMotionDetector>
                    </tns1:RuleEngine>
                </wstop:TopicSet>
                <wsnt:TopicExpressionDialect>http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet</wsnt:TopicExpressionDialect>
                <wsnt:TopicExpressionDialect>http://docs.oasis-open.org/wsn/t-1/TopicExpression/Concrete</wsnt:TopicExpressionDialect>
                <tev:MessageContentFilterDialect>http://www.onvif.org/ver10/tev/messageContentFilter/ItemFilter</tev:MessageContentFilterDialect>
                <tev:MessageContentSchemaLocation>http://www.onvif.org/onvif/ver10/schema/onvif.xsd</tev:MessageContentSchemaLocation>
            </tev:GetEventPropertiesResponse>
        '''

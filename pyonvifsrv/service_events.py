import re
import logging
import random
import datetime
from pyonvifsrv.context import Context

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
	def __init__(self, type: str, timestamp: datetime, payload: any):
		self.type = type
		self.timestamp = timestamp
		self.payload = payload

	def toXml(self) -> str:
		return '''
			<wsnt:NotificationMessage>
				<wsnt:Topic Dialect="http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet">{self.type}</wsnt:Topic>
				<wsnt:Message>
					<tt:Message xmlns:tt="http://www.onvif.org/ver10/schema">
						<tt:Source>
							<tt:SimpleItem Name="device" Value="{self.payload.device}" />
							<tt:SimpleItem Name="type" Value="{self.payload.type}" />
							<tt:SimpleItem Name="timestamp" Value="{self.timestamp.toISOString()}" />
						</tt:Source>
						<tt:Data>
							<tt:SimpleItem Name="data" Value="{self.payload.data}" />
						</tt:Data>
					</tt:Message>
				</wsnt:Message>
			</wsnt:NotificationMessage>
		'''

class PullPointSubscription():
    def __init__(self, id: str, expirationTime: datetime):
        self.id = id
        self.expirationTime: datetime = expirationTime
        self.messages: Message = []

    def addMessage(self, message: Message):
        self.messages.append(message)

class EventsService:
    def __init__(self, context: Context):
        self.context = context
        self.subscriptions = {}

    def createPullPointSubscription(self, data):
        listenIp = "10.10.10.70"
        listenPort = "10101"

        subscriptionId = str(random.randint(0, 2**32 - 1))

        initialTerminationTime: str = data["body"]["CreatePullPointSubscription"]["InitialTerminationTime"]
        expireInSeconds = getDurationAsSeconds(initialTerminationTime)
        logger.debug("Expire in seconds: {initialTerminationTime} - {expireInSeconds}".format(initialTerminationTime=initialTerminationTime, expireInSeconds=expireInSeconds))

        currentTime: datetime = datetime.datetime.now()
        expirationTime: datetime = currentTime + datetime.timedelta(seconds=expireInSeconds)

        subscription = PullPointSubscription(subscriptionId, expirationTime)

        self.subscriptions[subscriptionId] = subscription

        return '''
			<tev:CreatePullPointSubscriptionResponse>
				<tev:SubscriptionReference>
					<wsa5:Address>http://{listenIp}:{listenPort}/onvif/pullpoint/{subscriptionId}</wsa5:Address>
				</tev:SubscriptionReference>
				<wsnt:CurrentTime>{currentTime}</wsnt:CurrentTime>
				<wsnt:TerminationTime>{expirationTime}</wsnt:TerminationTime>
			</tev:CreatePullPointSubscriptionResponse>		
        '''.format(listenIp=listenIp, listenPort=listenPort, subscriptionId=subscriptionId, currentTime=currentTime.isoformat(), expirationTime=expirationTime.isoformat())

    def pullMessages(self, data):
        subscriptionId = data["body"]["PullMessages"]["SubscriptionReference"]["Address"].split("/")[-1]

        subscription = self.subscriptions[subscriptionId]

        messages = subscription.messages
        subscription.messages = []

        # messagesXml = subscription.messages.map(message => message.toXml()).join('')
        messagesXml = ''

        currentTime: datetime = datetime.datetime.now()
        terminationTime: datetime = subscription.expirationTime

        timeoutInSeconds = getDurationAsSeconds(data["body"]["PullMessages"]["Timeout"])

        # sleep(timeoutInSeconds)

        return '''
			<tev:PullMessagesResponse>
				<tev:CurrentTime>{currentTime}</tev:CurrentTime>
				<tev:TerminationTime>{terminationTime}</tev:TerminationTime>
				{messagesXml}
			</tev:PullMessagesResponse>
        '''.format(currentTime=currentTime.isoformat(), terminationTime=terminationTime.isoformat(), messagesXml=messagesXml)

    def renew(self, data):
        terminationTime: datetime = ""
        currentTime: datetime = ""

        return '''
			<wsnt:RenewResponse>
				<wsnt:TerminationTime>{terminationTime}</wsnt:TerminationTime>
				<wsnt:CurrentTime>{currentTime}</wsnt:CurrentTime>
			</wsnt:RenewResponse>
        '''.format(terminationTime=terminationTime.isoformat(), currentTime=currentTime.isoformat())

    def unsubscribe(self, data):
        return '''
            <wsnt:UnsubscribeResponse></wsnt:UnsubscribeResponse>        
        '''

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

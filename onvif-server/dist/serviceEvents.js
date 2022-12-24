"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.EventsService = void 0;
const util_1 = __importDefault(require("util"));
/*
function getDuration(years: number = 0, months: number = 0, days: number = 0, hours: number = 0, minutes: number = 0, seconds: number = 0): string {
    let duration = "P";
    if (years > 0) duration += `${years}Y`;
    if (months > 0) duration += `${months}M`;
    if (days > 0) duration += `${days}D`;
    if (hours > 0 || minutes > 0 || seconds > 0) duration += "T";
    if (hours > 0) duration += `${hours}H`;
    if (minutes > 0) duration += `${minutes}M`;
    if (seconds > 0) duration += `${seconds}S`;
    return duration;
}
*/
function getDurationFromSeconds(seconds) {
    const years = Math.floor(seconds / (365 * 24 * 60 * 60));
    seconds -= years * 365 * 24 * 60 * 60;
    const months = Math.floor(seconds / (30 * 24 * 60 * 60));
    seconds -= months * 30 * 24 * 60 * 60;
    const days = Math.floor(seconds / (24 * 60 * 60));
    seconds -= days * 24 * 60 * 60;
    const hours = Math.floor(seconds / (60 * 60));
    seconds -= hours * 60 * 60;
    const minutes = Math.floor(seconds / 60);
    seconds -= minutes * 60;
    let duration = "P";
    if (years > 0)
        duration += `${years}Y`;
    if (months > 0)
        duration += `${months}M`;
    if (days > 0)
        duration += `${days}D`;
    if (hours > 0 || minutes > 0 || seconds > 0)
        duration += "T";
    if (hours > 0)
        duration += `${hours}H`;
    if (minutes > 0)
        duration += `${minutes}M`;
    if (seconds > 0)
        duration += `${seconds}S`;
    return duration;
}
/*
function getDurationAsSeconds(duration: string): number {
    const yearsMatch = duration.match(/\d+Y/);
    const monthsMatch = duration.match(/\d+M/);
    const daysMatch = duration.match(/\d+D/);
    const hoursMatch = duration.match(/\d+H/);
    const minutesMatch = duration.match(/\d+M/);
    const secondsMatch = duration.match(/\d+S/);
  
    const years = yearsMatch ? parseInt(yearsMatch[0]) : 0;
    const months = monthsMatch ? parseInt(monthsMatch[0]) : 0;
    const days = daysMatch ? parseInt(daysMatch[0]) : 0;
    const hours = hoursMatch ? parseInt(hoursMatch[0]) : 0;
    const minutes = minutesMatch ? parseInt(minutesMatch[0]) : 0;
    const seconds = secondsMatch ? parseInt(secondsMatch[0]) : 0;
  
    return (years * 365 * 24 * 60 * 60) + (months * 30 * 24 * 60 * 60) + (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds;
}
*/
function getDurationAsSeconds(duration) {
    const regex = /^P((\d+Y)?(\d+M)?(\d+D)?)?(T(\d+H)?(\d+M)?(\d+S)?)?$/;
    const match = regex.exec(duration);
    if (!match) {
        throw new Error(`Invalid duration string: ${duration}`);
    }
    const years = parseInt(match[2]) || 0;
    const months = parseInt(match[3]) || 0;
    const days = parseInt(match[4]) || 0;
    const hours = parseInt(match[6]) || 0;
    const minutes = parseInt(match[7]) || 0;
    const seconds = parseInt(match[8]) || 0;
    // Note: this implementation doesn't take into account the actual number of days in a month,
    // so it may not be accurate for durations with months or years.
    return (years * 365 * 24 * 60 * 60) + (months * 30 * 24 * 60 * 60) + (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds;
}
async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
class EventsService {
    constructor(server) {
        this.serviceName = "events";
        this.interfaceName = "ens3";
        this.listenIp = "10.10.10.70";
        this.listenPort = "10101";
        this.serviceAddress = `http://${this.listenIp}:${this.listenPort}/onvif/services`;
        this.subscriptions = new Map();
        server.registerMethod(this.serviceName, 'createPullPointSubscription', (args) => this.createPullPointSubscription(args));
        server.registerMethod(this.serviceName, 'unsubscribe', (args, header) => this.unsubscribe(args, header));
        server.registerMethod(this.serviceName, 'pullMessages', async (args, header) => await this.pullMessages(args, header));
        server.registerMethod(this.serviceName, 'renew', (args, header) => this.renew(args, header));
        server.registerMethod(this.serviceName, 'getEventProperties', (args) => this.getEventProperties(args));
    }
    getSubscriptionIdFromToHeader(to) {
        let subscriptionId;
        if (to._) {
            subscriptionId = to._.substring(to._.lastIndexOf('/') + 1);
        }
        else {
            subscriptionId = to.substring(to.lastIndexOf('/') + 1);
        }
        console.log("subscriptionId: " + util_1.default.inspect(subscriptionId, false, null, true));
        return subscriptionId;
    }
    createPullPointSubscription(args) {
        console.log("createPullPointSubscription(): " + util_1.default.inspect(args, false, null, true));
        // Generate a subscription ID
        const subscriptionId = (Math.floor(Math.random() * Math.pow(2, 32))).toString();
        const currentTime = (new Date(Date.now()));
        const expirationTime = (new Date(currentTime));
        const expireInSeconds = getDurationAsSeconds(args["initialTerminationTime"]);
        expirationTime.setSeconds(expirationTime.getSeconds() + expireInSeconds);
        // Create a new PullPointSubscription instance
        const subscription = new PullPointSubscription(subscriptionId, expirationTime);
        // Add the subscription to the map
        this.subscriptions.set(subscriptionId, subscription);
        return `
			<tev:CreatePullPointSubscriptionResponse>
				<tev:SubscriptionReference>
					<wsa5:Address>http://${this.listenIp}:${this.listenPort}/onvif/pullpoint/${subscriptionId}</wsa5:Address>
				</tev:SubscriptionReference>
				<wsnt:CurrentTime>${currentTime.toISOString()}</wsnt:CurrentTime>
				<wsnt:TerminationTime>${expirationTime.toISOString()}</wsnt:TerminationTime>
			</tev:CreatePullPointSubscriptionResponse>		
		`;
    }
    unsubscribe(args, header) {
        const subscriptionId = this.getSubscriptionIdFromToHeader(header.to);
        console.log("unsubscribe(): " + util_1.default.inspect(args, false, null, true));
        // Look up the subscription in the map
        const subscription = this.subscriptions.get(subscriptionId);
        if (!subscription) {
            // Return an error if the subscription does not exist
            return `
				<soapenv:Fault>
					<soapenv:Code>
						<soapenv:Value>fault code</soapenv:Value>
							<soapenv:Subcode>
								<soapenv:Value>ter:fault subcode</soapenv:Value>
									<soapenv:Subcode>
										<soapenv:Value>ter:InvalidArgVal</soapenv:Value>
									</soapenv:Subcode>
							</soapenv:Subcode>
					</soapenv:Code>
				<soapenv:Reason>
					<soapenv:Text xml:lang="en">Subscription not found</soapenv:Text>
				</soapenv:Reason>
				<soapenv:Node>http://www.w3.org/2003/05/soap-envelope/node/ultimateReceiver</soapenv:Node>
				<soapenv:Role>http://www.w3.org/2003/05/soap-envelope/role/ultimateReceiver</soapenv:Role>
				<soapenv:Detail>
					<soapenv:Text>Subscription not found</soapenv:Text>
				</soapenv:Detail>
				</soapenv:Fault>			
			`;
        }
        // Remove the subscription from the map
        this.subscriptions.delete(subscriptionId);
        return `
			<wsnt:UnsubscribeResponse></wsnt:UnsubscribeResponse>
		`;
    }
    async pullMessages(args, header) {
        console.log("pullMessages(): " + util_1.default.inspect(args, false, null, true));
        //console.log("pullMessages(header): " + util.inspect(header, false, null, true));
        const subscriptionId = this.getSubscriptionIdFromToHeader(header.to);
        // Look up the subscription in the map
        const subscription = this.subscriptions.get(subscriptionId);
        if (!subscription) {
            // Return an error if the subscription does not exist
            return `
				<soapenv:Fault>
				<soapenv:Code>
					<soapenv:Value>fault code</soapenv:Value>
						<soapenv:Subcode>
							<soapenv:Value>ter:fault subcode</soapenv:Value>
								<soapenv:Subcode>
									<soapenv:Value>ter:InvalidArgVal</soapenv:Value>
								</soapenv:Subcode>
						</soapenv:Subcode>
				</soapenv:Code>
				<soapenv:Reason>
					<soapenv:Text xml:lang="en">Subscription not found</soapenv:Text>
				</soapenv:Reason>
				<soapenv:Node>http://www.w3.org/2003/05/soap-envelope/node/ultimateReceiver</soapenv:Node>
				<soapenv:Role>http://www.w3.org/2003/05/soap-envelope/role/ultimateReceiver</soapenv:Role>
				<soapenv:Detail>
					<soapenv:Text>Subscription not found</soapenv:Text>
				</soapenv:Detail>
				</soapenv:Fault>			
			`;
        }
        const messagesXml = subscription.messages.map(message => message.toXml()).join('');
        const currentTime = (new Date(Date.now()));
        const terminationTime = subscription.expirationTime;
        const timeoutInSeconds = getDurationAsSeconds(args["timeout"]);
        console.log("timeoutInSeconds: " + util_1.default.inspect(timeoutInSeconds, false, null, true));
        await sleep(timeoutInSeconds * 1000);
        return `
			<tev:PullMessagesResponse>
				<tev:CurrentTime>${currentTime.toISOString()}</tev:CurrentTime>
				<tev:TerminationTime>${terminationTime.toISOString()}</tev:TerminationTime>
				${messagesXml}
			</tev:PullMessagesResponse>
		`;
    }
    renew(args, header) {
        const subscriptionId = this.getSubscriptionIdFromToHeader(header.to);
        console.log("renew(): " + util_1.default.inspect(args, false, null, true));
        // Look up the subscription in the map
        const subscription = this.subscriptions.get(subscriptionId);
        if (!subscription) {
            // Return an error if the subscription does not exist
            return `
				<soapenv:Fault>
				<soapenv:Code>
					<soapenv:Value>fault code</soapenv:Value>
						<soapenv:Subcode>
							<soapenv:Value>ter:fault subcode</soapenv:Value>
								<soapenv:Subcode>
									<soapenv:Value>ter:InvalidArgVal</soapenv:Value>
								</soapenv:Subcode>
						</soapenv:Subcode>
				</soapenv:Code>
				<soapenv:Reason>
					<soapenv:Text xml:lang="en">Subscription not found</soapenv:Text>
				</soapenv:Reason>
				<soapenv:Node>http://www.w3.org/2003/05/soap-envelope/node/ultimateReceiver</soapenv:Node>
				<soapenv:Role>http://www.w3.org/2003/05/soap-envelope/role/ultimateReceiver</soapenv:Role>
				<soapenv:Detail>
					<soapenv:Text>Subscription not found</soapenv:Text>
				</soapenv:Detail>
				</soapenv:Fault>			
			`;
        }
        const currentTime = (new Date(Date.now()));
        const terminationTime = (new Date(currentTime));
        const terminationTimeInSeconds = getDurationAsSeconds(args["terminationTime"]);
        terminationTime.setSeconds(terminationTime.getSeconds() + terminationTimeInSeconds);
        subscription.expirationTime = terminationTime;
        return `
			<wsnt:RenewResponse>
				<wsnt:TerminationTime>${terminationTime.toISOString()}</wsnt:TerminationTime>
				<wsnt:CurrentTime>${currentTime.toISOString()}</wsnt:CurrentTime>
			</wsnt:RenewResponse>
		`;
    }
    getEventProperties(args) {
        console.log("getEventProperties(): " + util_1.default.inspect(args, false, null, true));
        return `
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
		`;
    }
}
exports.EventsService = EventsService;
class PullPointSubscription {
    constructor(id, expirationTime) {
        this.messages = [];
        this.id = id;
        this.expirationTime = expirationTime;
    }
    addMessage(message) {
        this.messages.push(message);
    }
}
class Message {
    constructor(type, timestamp, payload) {
        this.type = type;
        this.timestamp = timestamp;
        this.payload = payload;
    }
    toXml() {
        return `
			<wsnt:NotificationMessage>
				<wsnt:Topic Dialect="http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet">${this.type}</wsnt:Topic>
				<wsnt:Message>
					<tt:Message xmlns:tt="http://www.onvif.org/ver10/schema">
						<tt:Source>
							<tt:SimpleItem Name="device" Value="${this.payload.device}" />
							<tt:SimpleItem Name="type" Value="${this.payload.type}" />
							<tt:SimpleItem Name="timestamp" Value="${this.timestamp.toISOString()}" />
						</tt:Source>
						<tt:Data>
							<tt:SimpleItem Name="data" Value="${this.payload.data}" />
						</tt:Data>
					</tt:Message>
				</wsnt:Message>
			</wsnt:NotificationMessage>
		`;
    }
}
//# sourceMappingURL=serviceEvents.js.map
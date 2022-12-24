"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.DeviceService = void 0;
const util_1 = __importDefault(require("util"));
class DeviceService {
    constructor(server) {
        this.serviceName = "device";
        this.interfaceName = "ens3";
        this.listenIp = "10.10.10.70";
        this.listenPort = "10101";
        this.serviceAddress = `http://${this.listenIp}:${this.listenPort}/onvif/services`;
        server.registerMethod(this.serviceName, 'getSystemDateAndTime', (args) => this.getSystemDateAndTime(args));
        server.registerMethod(this.serviceName, 'getScopes', (args) => this.getScopes(args));
        server.registerMethod(this.serviceName, 'getDeviceInformation', (args) => this.getDeviceInformation(args));
        server.registerMethod(this.serviceName, 'getNetworkInterfaces', (args) => this.getNetworkInterfaces(args));
        server.registerMethod(this.serviceName, 'getDNS', (args) => this.getDNS(args));
        server.registerMethod(this.serviceName, 'getServices', (args) => this.getServices(args));
        server.registerMethod(this.serviceName, 'getCapabilities', (args) => this.getCapabilities(args));
        server.registerMethod(this.serviceName, 'getZeroConfiguration', (args) => this.getZeroConfiguration(args));
        server.registerMethod(this.serviceName, 'getServiceCapabilities', (args) => this.getServiceCapabilities(args));
        server.registerMethod(this.serviceName, 'getNTP', (args) => this.getNTP(args));
        server.registerMethod(this.serviceName, 'getNetworkDefaultGateway', (args) => this.getNetworkDefaultGateway(args));
        server.registerMethod(this.serviceName, 'getNetworkProtocols', (args) => this.getNetworkProtocols(args));
        server.registerMethod(this.serviceName, 'getHostname', (args) => this.getHostname(args));
        server.registerMethod(this.serviceName, 'getDiscoveryMode', (args) => this.getDiscoveryMode(args));
        server.registerMethod(this.serviceName, 'getUsers', (args) => this.getUsers(args));
        server.registerMethod(this.serviceName, 'getCertificates', (args) => this.getCertificates(args));
        server.registerMethod(this.serviceName, 'getCertificatesStatus', (args) => this.getCertificatesStatus(args));
        server.registerMethod(this.serviceName, 'getRelayOutputs', (args) => this.getRelayOutputs(args));
        server.registerMethod(this.serviceName, 'setSystemFactoryDefault', (args) => this.setSystemFactoryDefault(args));
        server.registerMethod(this.serviceName, 'systemReboot', (args) => this.systemReboot(args));
    }
    getSystemDateAndTime(args) {
        console.log("getSystemDateAndTime(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetSystemDateAndTimeResponse>
				<tds:SystemDateAndTime>
					<tt:DateTimeType>Manual</tt:DateTimeType>
					<tt:DaylightSavings>true</tt:DaylightSavings>
					<tt:TimeZone>
						<tt:TZ>WEuropeStandardTime-1DaylightTime,M3.5.0,M10.5.0/3</tt:TZ>
					</tt:TimeZone>
					<tt:UTCDateTime>
						<tt:Time>
							<tt:Hour>19</tt:Hour>
							<tt:Minute>14</tt:Minute>
							<tt:Second>37</tt:Second>
						</tt:Time>
						<tt:Date>
							<tt:Year>2014</tt:Year>
							<tt:Month>12</tt:Month>
							<tt:Day>24</tt:Day>
						</tt:Date>
					</tt:UTCDateTime>
				</tds:SystemDateAndTime>
			</tds:GetSystemDateAndTimeResponse>		
		`;
    }
    getScopes(args) {
        console.log("getScopes(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetScopesResponse>
				<tds:Scopes>
					<tt:ScopeDef>Fixed</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/Profile/Streaming</tt:ScopeItem>
				</tds:Scopes>
				<tds:Scopes>
					<tt:ScopeDef>Fixed</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/Profile/T</tt:ScopeItem>
				</tds:Scopes>
				<tds:Scopes>
					<tt:ScopeDef>Fixed</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/type/video_encoder</tt:ScopeItem>
				</tds:Scopes>
				<tds:Scopes>
					<tt:ScopeDef>Fixed</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/type/audio_encoder</tt:ScopeItem>
				</tds:Scopes>
				<tds:Scopes>
					<tt:ScopeDef>Fixed</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/type/ptz</tt:ScopeItem>
				</tds:Scopes>
				<tds:Scopes>
					<tt:ScopeDef>Fixed</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/hardware/HD_PREDATOR</tt:ScopeItem>
				</tds:Scopes>
				<tds:Scopes>
					<tt:ScopeDef>Configurable</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/name/PREDATOR</tt:ScopeItem>
				</tds:Scopes>
				<tds:Scopes>
					<tt:ScopeDef>Configurable</tt:ScopeDef>
					<tt:ScopeItem>onvif://www.onvif.org/location/</tt:ScopeItem>
				</tds:Scopes>
			</tds:GetScopesResponse>		
		`;
        // <tds:Scopes>
        // 	<tt:ScopeDef>Fixed</tt:ScopeDef>
        // 	<tt:ScopeItem>onvif://www.onvif.org/Profile/T</tt:ScopeItem>
        // </tds:Scopes>		
    }
    getDeviceInformation(args) {
        console.log("getDeviceInformation(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetDeviceInformationResponse>
				<tds:Manufacturer>Mockup Manufacturer</tds:Manufacturer>
				<tds:Model>Mockup Model</tds:Model>
				<tds:FirmwareVersion>Mockup_15_14_13</tds:FirmwareVersion>
				<tds:SerialNumber>00000000</tds:SerialNumber>
				<tds:HardwareId>MOCKUP</tds:HardwareId>
			</tds:GetDeviceInformationResponse>		
		`;
    }
    getNetworkInterfaces(args) {
        console.log("getNetworkInterfaces(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:SetNetworkInterfacesResponse>
				<tds:RebootNeeded>false</tds:RebootNeeded>
			</tds:SetNetworkInterfacesResponse>
		`;
    }
    getDNS(args) {
        console.log("getDNS(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetDNSResponse>
				<tds:DNSInformation>
					<tt:FromDHCP>false</tt:FromDHCP>
					<tt:DNSManual>
						<tt:Type>IPv4</tt:Type>
						<tt:IPv4Address>4.4.4.4</tt:IPv4Address>
					</tt:DNSManual>
					<tt:DNSManual>
						<tt:Type>IPv4</tt:Type>
						<tt:IPv4Address>8.8.8.8</tt:IPv4Address>
					</tt:DNSManual>
				</tds:DNSInformation>
			</tds:GetDNSResponse>
		`;
    }
    getServices(args) {
        console.log("getServices(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetServicesResponse>
				<tds:Service>
					<tds:Namespace>http://www.onvif.org/ver10/device/wsdl</tds:Namespace>
					<tds:XAddr>${this.serviceAddress}</tds:XAddr>
					<tds:Version>
						<tt:Major>2</tt:Major>
						<tt:Minor>42</tt:Minor>
					</tds:Version>
				</tds:Service>
				<tds:Service>
					<tds:Namespace>http://www.onvif.org/ver10/media/wsdl</tds:Namespace>
					<tds:XAddr>${this.serviceAddress}</tds:XAddr>
					<tds:Version>
						<tt:Major>2</tt:Major>
						<tt:Minor>41</tt:Minor>
					</tds:Version>
				</tds:Service>
				<tds:Service>
					<tds:Namespace>http://www.onvif.org/ver10/events/wsdl</tds:Namespace>
					<tds:XAddr>${this.serviceAddress}</tds:XAddr>
					<tds:Version>
						<tt:Major>2</tt:Major>
						<tt:Minor>40</tt:Minor>
					</tds:Version>
				</tds:Service>
				<tds:Service>
					<tds:Namespace>http://www.onvif.org/ver10/deviceIO/wsdl</tds:Namespace>
					<tds:XAddr>${this.serviceAddress}</tds:XAddr>
					<tds:Version>
						<tt:Major>2</tt:Major>
						<tt:Minor>20</tt:Minor>
					</tds:Version>
				</tds:Service>
				<tds:Service>
					<tds:Namespace>http://www.onvif.org/ver20/ptz/wsdl</tds:Namespace>
					<tds:XAddr>${this.serviceAddress}</tds:XAddr>
					<tds:Version>
						<tt:Major>2</tt:Major>
						<tt:Minor>41</tt:Minor>
					</tds:Version>
				</tds:Service>
				<tds:Service>
					<tds:Namespace>http://www.onvif.org/ver20/imaging/wsdl</tds:Namespace>
					<tds:XAddr>${this.serviceAddress}</tds:XAddr>
					<tds:Version>
						<tt:Major>2</tt:Major>
						<tt:Minor>30</tt:Minor>
					</tds:Version>
				</tds:Service>
			</tds:GetServicesResponse>		
		`;
    }
    getCapabilities(args) {
        console.log("getCapabilities(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetCapabilitiesResponse>
				<tds:Capabilities>
					<tt:Device>
						<tt:XAddr>${this.serviceAddress}</tt:XAddr>
						<tt:Network>
							<tt:IPFilter>false</tt:IPFilter>
							<tt:ZeroConfiguration>true</tt:ZeroConfiguration>
							<tt:IPVersion6>false</tt:IPVersion6>
							<tt:DynDNS>false</tt:DynDNS>
						</tt:Network>
						<tt:System>
							<tt:DiscoveryResolve>false</tt:DiscoveryResolve>
							<tt:DiscoveryBye>false</tt:DiscoveryBye>
							<tt:RemoteDiscovery>false</tt:RemoteDiscovery>
							<tt:SystemBackup>false</tt:SystemBackup>
							<tt:SystemLogging>false</tt:SystemLogging>
							<tt:FirmwareUpgrade>false</tt:FirmwareUpgrade>
							<tt:SupportedVersions>
								<tt:Major>2</tt:Major>
								<tt:Minor>40</tt:Minor>
							</tt:SupportedVersions>
						</tt:System>
						<tt:IO>
							<tt:InputConnectors>1</tt:InputConnectors>
							<tt:RelayOutputs>1</tt:RelayOutputs>
						</tt:IO>
						<tt:Security>
							<tt:TLS1.1>true</tt:TLS1.1>
							<tt:TLS1.2>false</tt:TLS1.2>
							<tt:OnboardKeyGeneration>false</tt:OnboardKeyGeneration>
							<tt:AccessPolicyConfig>false</tt:AccessPolicyConfig>
							<tt:X.509Token>false</tt:X.509Token>
							<tt:SAMLToken>false</tt:SAMLToken>
							<tt:KerberosToken>false</tt:KerberosToken>
							<tt:RELToken>false</tt:RELToken>
						</tt:Security>
					</tt:Device>
					<tt:Events>
						<tt:XAddr>${this.serviceAddress}</tt:XAddr>
						<tt:WSSubscriptionPolicySupport>false</tt:WSSubscriptionPolicySupport>
						<tt:WSPullPointSupport>true</tt:WSPullPointSupport>
						<tt:WSPausableSubscriptionManagerInterfaceSupport>false</tt:WSPausableSubscriptionManagerInterfaceSupport>
					</tt:Events>
					<tt:Imaging>
						<tt:XAddr>${this.serviceAddress}</tt:XAddr>
					</tt:Imaging>
					<tt:Media>
						<tt:XAddr>${this.serviceAddress}</tt:XAddr>
						<tt:StreamingCapabilities>
							<tt:RTPMulticast>false</tt:RTPMulticast>
							<tt:RTP_TCP>true</tt:RTP_TCP>
							<tt:RTP_RTSP_TCP>true</tt:RTP_RTSP_TCP>
						</tt:StreamingCapabilities>
					</tt:Media>
					<tt:PTZ>
						<tt:XAddr>${this.serviceAddress}</tt:XAddr>
					</tt:PTZ>
					<tt:Extension>
						<tt:DeviceIO>
							<tt:XAddr>${this.serviceAddress}</tt:XAddr>
							<tt:VideoSources>1</tt:VideoSources>
							<tt:VideoOutputs>0</tt:VideoOutputs>
							<tt:AudioSources>1</tt:AudioSources>
							<tt:AudioOutputs>1</tt:AudioOutputs>
							<tt:RelayOutputs>1</tt:RelayOutputs>
						</tt:DeviceIO>
					</tt:Extension>
				</tds:Capabilities>
			</tds:GetCapabilitiesResponse>
		`;
    }
    getZeroConfiguration(args) {
        console.log("getZeroConfiguration(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetZeroConfigurationResponse>
				<tds:ZeroConfiguration>
					<tt:InterfaceToken>${this.interfaceName}</tt:InterfaceToken>
					<tt:Enabled>true</tt:Enabled>
					<tt:Addresses>${this.listenIp}</tt:Addresses>
				</tds:ZeroConfiguration>
			</tds:GetZeroConfigurationResponse>
		`;
    }
    getServiceCapabilities(args) {
        console.log("getServiceCapabilities(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetServiceCapabilitiesResponse>
				<tds:Capabilities>
					<tds:Network DHCPv6="false" NTP="1" HostnameFromDHCP="false" Dot1XConfigurations="0" Dot11Configuration="false" DynDNS="false" IPVersion6="false" ZeroConfiguration="true" IPFilter="false"></tds:Network>
					<tds:Security RELToken="false" HttpDigest="false" UsernameToken="true" KerberosToken="false" SAMLToken="false" X.509Token="false" RemoteUserHandling="false" Dot1X="false" DefaultAccessPolicy="false" AccessPolicyConfig="false" OnboardKeyGeneration="false" TLS1.2="false" TLS1.1="false" TLS1.0="false"></tds:Security>
					<tds:System HttpSupportInformation="false" HttpSystemLogging="false" HttpSystemBackup="false" HttpFirmwareUpgrade="false" FirmwareUpgrade="false" SystemLogging="false" SystemBackup="false" RemoteDiscovery="false" DiscoveryBye="true" DiscoveryResolve="false"></tds:System>
					<tds:Misc AuxiliaryCommands="AUX1 AUX2 AUX3 AUX4 AUX5 AUX6 AUX7 AUX8"></tds:Misc>
				</tds:Capabilities>
			</tds:GetServiceCapabilitiesResponse>
		`;
    }
    setSystemFactoryDefault(args) {
        console.log("setSystemFactoryDefault(): " + util_1.default.inspect(args, false, null, true));
        return `
	        <tds:SetSystemFactoryDefaultResponse></tds:SetSystemFactoryDefaultResponse>
		`;
    }
    systemReboot(args) {
        console.log("systemReboot(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:SystemRebootResponse>
				<tds:Message>Reboot in 30 secs</tds:Message>
			</tds:SystemRebootResponse>
		`;
    }
    getNTP(args) {
        console.log("getNTP(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetNTPResponse>
				<tds:NTPInformation>
					<tt:FromDHCP>false</tt:FromDHCP>
					<tt:NTPManual>
						<tt:Type>IPv4</tt:Type>
						<tt:IPv4Address>192.168.1.168</tt:IPv4Address>
					</tt:NTPManual>
				</tds:NTPInformation>
			</tds:GetNTPResponse>
		`;
    }
    getNetworkDefaultGateway(args) {
        console.log("getNetworkDefaultGateway(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetNetworkDefaultGatewayResponse>
				<tds:NetworkGateway>
					<tds:IPv4Address>192.168.0.1</tds:IPv4Address>
					<tds:IPv6Address></tds:IPv6Address>
				</tds:NetworkGateway>
			</tds:GetNetworkDefaultGatewayResponse>
		`;
    }
    getNetworkProtocols(args) {
        console.log("getNetworkProtocols(): " + util_1.default.inspect(args, false, null, true));
        return `
		`;
    }
    getHostname(args) {
        console.log("getHostname(): " + util_1.default.inspect(args, false, null, true));
        return `
			<tds:GetHostnameResponse>
				<tds:HostnameInformation>
					<tt:FromDHCP>false</tt:FromDHCP>
					<tt:Name>IPNC-RDK</tt:Name>
				</tds:HostnameInformation>
			</tds:GetHostnameResponse>
		`;
    }
    getDiscoveryMode(args) {
        console.log("getDiscoveryMode(): " + util_1.default.inspect(args, false, null, true));
        return `
		`;
    }
    getUsers(args) {
        console.log("getUsers(): " + util_1.default.inspect(args, false, null, true));
        return `
		`;
    }
    getCertificates(args) {
        console.log("getCertificates(): " + util_1.default.inspect(args, false, null, true));
        return `
		`;
    }
    getCertificatesStatus(args) {
        console.log("getCertificatesStatus(): " + util_1.default.inspect(args, false, null, true));
        return `
		`;
    }
    getRelayOutputs(args) {
        console.log("getRelayOutputs(): " + util_1.default.inspect(args, false, null, true));
        return `
		`;
    }
}
exports.DeviceService = DeviceService;
//# sourceMappingURL=serviceDevice.js.map
import util from "util";
import { OnvifServer } from "./serverMockup";

export class DeviceService {

	public readonly serviceName = "device";
	public interfaceName = "ens3";
	public listenIp = "10.10.10.70";
	public listenPort = "10101";
	public serviceAddress = `http://${this.listenIp}:${this.listenPort}/onvif/services`;

	constructor(server: OnvifServer) {
		server.registerMethod(this.serviceName, 'getSystemDateAndTime', (args: any) => this.getSystemDateAndTime(args));
		server.registerMethod(this.serviceName, 'getScopes', (args: any) => this.getScopes(args));
		server.registerMethod(this.serviceName, 'getDeviceInformation', (args: any) => this.getDeviceInformation(args));
		server.registerMethod(this.serviceName, 'getNetworkInterfaces', (args: any) => this.getNetworkInterfaces(args));
		server.registerMethod(this.serviceName, 'getDNS', (args: any) => this.getDNS(args));
		server.registerMethod(this.serviceName, 'getServices', (args: any) => this.getServices(args));
		server.registerMethod(this.serviceName, 'getCapabilities', (args: any) => this.getCapabilities(args));
		server.registerMethod(this.serviceName, 'getZeroConfiguration', (args: any) => this.getZeroConfiguration(args));
		server.registerMethod(this.serviceName, 'getServiceCapabilities', (args: any) => this.getServiceCapabilities(args));
		server.registerMethod(this.serviceName, 'getNTP', (args: any) => this.getNTP(args));
		server.registerMethod(this.serviceName, 'getNetworkDefaultGateway', (args: any) => this.getNetworkDefaultGateway(args));
		server.registerMethod(this.serviceName, 'getNetworkProtocols', (args: any) => this.getNetworkProtocols(args));
		server.registerMethod(this.serviceName, 'getHostname', (args: any) => this.getHostname(args));
		server.registerMethod(this.serviceName, 'getDiscoveryMode', (args: any) => this.getDiscoveryMode(args));
		server.registerMethod(this.serviceName, 'getUsers', (args: any) => this.getUsers(args));
		server.registerMethod(this.serviceName, 'getCertificates', (args: any) => this.getCertificates(args));
		server.registerMethod(this.serviceName, 'getCertificatesStatus', (args: any) => this.getCertificatesStatus(args));
		server.registerMethod(this.serviceName, 'getRelayOutputs', (args: any) => this.getRelayOutputs(args));

		server.registerMethod(this.serviceName, 'setSystemFactoryDefault', (args: any) => this.setSystemFactoryDefault(args));
		server.registerMethod(this.serviceName, 'systemReboot', (args: any) => this.systemReboot(args));
	}

	private getSystemDateAndTime(args: any): string {

		console.log("getSystemDateAndTime(): " + util.inspect(args, false, null, true));
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

	private getScopes(args: any): string {

		console.log("getScopes(): " + util.inspect(args, false, null, true));
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

	private getDeviceInformation(args: any): string {

		console.log("getDeviceInformation(): " + util.inspect(args, false, null, true));
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

	private getNetworkInterfaces(args: any): string {

		console.log("getNetworkInterfaces(): " + util.inspect(args, false, null, true));
		return `
			<tds:SetNetworkInterfacesResponse>
				<tds:RebootNeeded>false</tds:RebootNeeded>
			</tds:SetNetworkInterfacesResponse>
		`;
	}

	private getDNS(args: any): string {

		console.log("getDNS(): " + util.inspect(args, false, null, true));
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

	private getServices(args: any): string {

		console.log("getServices(): " + util.inspect(args, false, null, true));
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

	private getCapabilities(args: any): string {

		console.log("getCapabilities(): " + util.inspect(args, false, null, true));
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
	private getZeroConfiguration(args: any): string {

		console.log("getZeroConfiguration(): " + util.inspect(args, false, null, true));
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

	private getServiceCapabilities(args: any): string {

		console.log("getServiceCapabilities(): " + util.inspect(args, false, null, true));
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

	private setSystemFactoryDefault(args: any): string {

		console.log("setSystemFactoryDefault(): " + util.inspect(args, false, null, true));
		return `
	        <tds:SetSystemFactoryDefaultResponse></tds:SetSystemFactoryDefaultResponse>
		`;
	}

	private systemReboot(args: any): string {

		console.log("systemReboot(): " + util.inspect(args, false, null, true));
		return `
			<tds:SystemRebootResponse>
				<tds:Message>Reboot in 30 secs</tds:Message>
			</tds:SystemRebootResponse>
		`;
	}

	private getNTP(args: any): string {

		console.log("getNTP(): " + util.inspect(args, false, null, true));
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

	private getNetworkDefaultGateway(args: any): string {

		console.log("getNetworkDefaultGateway(): " + util.inspect(args, false, null, true));
		return `
			<tds:GetNetworkDefaultGatewayResponse>
				<tds:NetworkGateway>
					<tds:IPv4Address>192.168.0.1</tds:IPv4Address>
					<tds:IPv6Address></tds:IPv6Address>
				</tds:NetworkGateway>
			</tds:GetNetworkDefaultGatewayResponse>
		`;
	}

	private getNetworkProtocols(args: any): string {

		console.log("getNetworkProtocols(): " + util.inspect(args, false, null, true));
		return `
		`;
	}

	private getHostname(args: any): string {

		console.log("getHostname(): " + util.inspect(args, false, null, true));
		return `
			<tds:GetHostnameResponse>
				<tds:HostnameInformation>
					<tt:FromDHCP>false</tt:FromDHCP>
					<tt:Name>IPNC-RDK</tt:Name>
				</tds:HostnameInformation>
			</tds:GetHostnameResponse>
		`;
	}

	private getDiscoveryMode(args: any): string {

		console.log("getDiscoveryMode(): " + util.inspect(args, false, null, true));
		return `
		`;
	}

	private getUsers(args: any): string {

		console.log("getUsers(): " + util.inspect(args, false, null, true));
		return `
		`;
	}

	private getCertificates(args: any): string {

		console.log("getCertificates(): " + util.inspect(args, false, null, true));
		return `
		`;
	}

	private getCertificatesStatus(args: any): string {

		console.log("getCertificatesStatus(): " + util.inspect(args, false, null, true));
		return `
		`;
	}

	private getRelayOutputs(args: any): string {

		console.log("getRelayOutputs(): " + util.inspect(args, false, null, true));
		return `
		`;
	}

}

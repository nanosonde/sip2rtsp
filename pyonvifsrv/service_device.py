import logging
from pyonvifsrv.context import Context

logger = logging.getLogger(__name__)

class DeviceService:
    def __init__(self, context: Context):
        self.context = context

    def getSystemDateAndTime(self, data):
        return '''
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
        '''

    def getScopes(self, data):
        # <tds:Scopes>
        # 	<tt:ScopeDef>Fixed</tt:ScopeDef>
        # 	<tt:ScopeItem>onvif://www.onvif.org/Profile/T</tt:ScopeItem>
        # </tds:Scopes>
        return '''
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
        '''

    def getDeviceInformation(self, data):
        return '''
            <tds:GetDeviceInformationResponse>
                <tds:Manufacturer>Mockup Manufacturer</tds:Manufacturer>
                <tds:Model>Mockup Model</tds:Model>
                <tds:FirmwareVersion>Mockup_15_14_13</tds:FirmwareVersion>
                <tds:SerialNumber>00000000</tds:SerialNumber>
                <tds:HardwareId>MOCKUP</tds:HardwareId>
            </tds:GetDeviceInformationResponse>		
        '''

    def getCapabilities(self, data):
        return '''
            <tds:GetCapabilitiesResponse>
                <tds:Capabilities>
                    <tt:Device>
                        <tt:XAddr>{serviceAddress}</tt:XAddr>
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
                        <tt:XAddr>{serviceAddress}</tt:XAddr>
                        <tt:WSSubscriptionPolicySupport>false</tt:WSSubscriptionPolicySupport>
                        <tt:WSPullPointSupport>true</tt:WSPullPointSupport>
                        <tt:WSPausableSubscriptionManagerInterfaceSupport>false</tt:WSPausableSubscriptionManagerInterfaceSupport>
                    </tt:Events>
                    <tt:Imaging>
                        <tt:XAddr>{serviceAddress}</tt:XAddr>
                    </tt:Imaging>
                    <tt:Media>
                        <tt:XAddr>{serviceAddress}</tt:XAddr>
                        <tt:StreamingCapabilities>
                            <tt:RTPMulticast>false</tt:RTPMulticast>
                            <tt:RTP_TCP>true</tt:RTP_TCP>
                            <tt:RTP_RTSP_TCP>true</tt:RTP_RTSP_TCP>
                        </tt:StreamingCapabilities>
                    </tt:Media>
                    <tt:PTZ>
                        <tt:XAddr>{serviceAddress}</tt:XAddr>
                    </tt:PTZ>
                    <tt:Extension>
                        <tt:DeviceIO>
                            <tt:XAddr>{serviceAddress}</tt:XAddr>
                            <tt:VideoSources>1</tt:VideoSources>
                            <tt:VideoOutputs>0</tt:VideoOutputs>
                            <tt:AudioSources>1</tt:AudioSources>
                            <tt:AudioOutputs>1</tt:AudioOutputs>
                            <tt:RelayOutputs>1</tt:RelayOutputs>
                        </tt:DeviceIO>
                    </tt:Extension>
                </tds:Capabilities>
            </tds:GetCapabilitiesResponse>
        '''.format(serviceAddress=self.context.serviceAddress)

    def getServices(self, data):
        return '''
            <tds:GetServicesResponse>
                <tds:Service>
                    <tds:Namespace>http://www.onvif.org/ver10/device/wsdl</tds:Namespace>
                    <tds:XAddr>{serviceAddress}</tds:XAddr>
                    <tds:Version>
                        <tt:Major>2</tt:Major>
                        <tt:Minor>42</tt:Minor>
                    </tds:Version>
                </tds:Service>
                <tds:Service>
                    <tds:Namespace>http://www.onvif.org/ver10/media/wsdl</tds:Namespace>
                    <tds:XAddr>{serviceAddress}</tds:XAddr>
                    <tds:Version>
                        <tt:Major>2</tt:Major>
                        <tt:Minor>41</tt:Minor>
                    </tds:Version>
                </tds:Service>
                <tds:Service>
                    <tds:Namespace>http://www.onvif.org/ver10/events/wsdl</tds:Namespace>
                    <tds:XAddr>{serviceAddress}</tds:XAddr>
                    <tds:Version>
                        <tt:Major>2</tt:Major>
                        <tt:Minor>40</tt:Minor>
                    </tds:Version>
                </tds:Service>
                <tds:Service>
                    <tds:Namespace>http://www.onvif.org/ver10/deviceIO/wsdl</tds:Namespace>
                    <tds:XAddr>{serviceAddress}</tds:XAddr>
                    <tds:Version>
                        <tt:Major>2</tt:Major>
                        <tt:Minor>20</tt:Minor>
                    </tds:Version>
                </tds:Service>
                <tds:Service>
                    <tds:Namespace>http://www.onvif.org/ver20/ptz/wsdl</tds:Namespace>
                    <tds:XAddr>{serviceAddress}</tds:XAddr>
                    <tds:Version>
                        <tt:Major>2</tt:Major>
                        <tt:Minor>41</tt:Minor>
                    </tds:Version>
                </tds:Service>
                <tds:Service>
                    <tds:Namespace>http://www.onvif.org/ver20/imaging/wsdl</tds:Namespace>
                    <tds:XAddr>{serviceAddress}</tds:XAddr>
                    <tds:Version>
                        <tt:Major>2</tt:Major>
                        <tt:Minor>30</tt:Minor>
                    </tds:Version>
                </tds:Service>
            </tds:GetServicesResponse>		
        '''.format(serviceAddress=self.context.serviceAddress)

    def getHostname(self, data):
        hostname = "IPNC-RDK"
        return '''
			<tds:GetHostnameResponse>
				<tds:HostnameInformation>
					<tt:FromDHCP>false</tt:FromDHCP>
					<tt:Name>{hostname}</tt:Name>
				</tds:HostnameInformation>
			</tds:GetHostnameResponse>
        '''.format(hostname=hostname)

    def getDNS(self, data):
        return '''
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
        '''
    def getNetworkInterfaces(self, data):
        return '''
            <tds:SetNetworkInterfacesResponse>
                <tds:RebootNeeded>false</tds:RebootNeeded>
            </tds:SetNetworkInterfacesResponse>
        '''

    def getZeroConfiguration(self, data):
        listenIp = "10.10.10.70"
        interfaceName = "ens3"
        return '''
            <tds:GetZeroConfigurationResponse>
                <tds:ZeroConfiguration>
                    <tt:InterfaceToken>{interfaceName}</tt:InterfaceToken>
                    <tt:Enabled>true</tt:Enabled>
                    <tt:Addresses>{listenIp}</tt:Addresses>
                </tds:ZeroConfiguration>
            </tds:GetZeroConfigurationResponse>
        '''.format(interfaceName=interfaceName, listenIp=listenIp)

    def getNTP(self, data):
        return '''
			<tds:GetNTPResponse>
				<tds:NTPInformation>
					<tt:FromDHCP>false</tt:FromDHCP>
					<tt:NTPManual>
						<tt:Type>IPv4</tt:Type>
						<tt:IPv4Address>192.168.1.168</tt:IPv4Address>
					</tt:NTPManual>
				</tds:NTPInformation>
			</tds:GetNTPResponse>
        '''

    def getNetworkDefaultGateway(self, data):
        return '''
			<tds:GetNetworkDefaultGatewayResponse>
				<tds:NetworkGateway>
					<tds:IPv4Address>192.168.0.1</tds:IPv4Address>
					<tds:IPv6Address></tds:IPv6Address>
				</tds:NetworkGateway>
			</tds:GetNetworkDefaultGatewayResponse>
        '''

    def getNetworkProtocols(self, data):
        return '''
        '''

    def getDiscoveryMode(self, data):
        return '''
        '''

    def getUsers(self, data):
        return '''
        '''

    def getCertificates(self, data):
        return '''
        '''

    def getCertificatesStatus(self, data):
        return '''
        '''

    def getServiceCapabilities(self, data):
        return '''
			<tds:GetServiceCapabilitiesResponse>
				<tds:Capabilities>
					<tds:Network DHCPv6="false" NTP="1" HostnameFromDHCP="false" Dot1XConfigurations="0" Dot11Configuration="false" DynDNS="false" IPVersion6="false" ZeroConfiguration="true" IPFilter="false"></tds:Network>
					<tds:Security RELToken="false" HttpDigest="false" UsernameToken="true" KerberosToken="false" SAMLToken="false" X.509Token="false" RemoteUserHandling="false" Dot1X="false" DefaultAccessPolicy="false" AccessPolicyConfig="false" OnboardKeyGeneration="false" TLS1.2="false" TLS1.1="false" TLS1.0="false"></tds:Security>
					<tds:System HttpSupportInformation="false" HttpSystemLogging="false" HttpSystemBackup="false" HttpFirmwareUpgrade="false" FirmwareUpgrade="false" SystemLogging="false" SystemBackup="false" RemoteDiscovery="false" DiscoveryBye="true" DiscoveryResolve="false"></tds:System>
					<tds:Misc AuxiliaryCommands="AUX1 AUX2 AUX3 AUX4 AUX5 AUX6 AUX7 AUX8"></tds:Misc>
				</tds:Capabilities>
			</tds:GetServiceCapabilitiesResponse>
        '''

    def setSystemFactoryDefault(self, data):
        return '''
            <tds:SetSystemFactoryDefaultResponse>
                <tds:RebootNeeded>true</tds:RebootNeeded>
            </tds:SetSystemFactoryDefaultResponse>
        '''

    def systemReboot(self, data):
        return '''
			<tds:SystemRebootResponse>
				<tds:Message>Reboot in 30 secs</tds:Message>
			</tds:SystemRebootResponse>
        '''
    def setDiscoveryMode(self, data):
        return '''
            <tds:SetDiscoveryModeResponse>
            </tds:SetDiscoveryModeResponse>
        '''

    def getRelayOutputs(self, data):
        return '''
        '''

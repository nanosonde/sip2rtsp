import logging
from pyonvifsrv.context import Context

logger = logging.getLogger(__name__)

class DeviceService:
    def __init__(self, context: Context):
        self.context = context

    def getSystemDateAndTime(self, data):
        logger.info("getSystemDateAndTime()")
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
        logger.info("getScopes()")
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
				# <tds:Scopes>
				# 	<tt:ScopeDef>Fixed</tt:ScopeDef>
				# 	<tt:ScopeItem>onvif://www.onvif.org/Profile/T</tt:ScopeItem>
				# </tds:Scopes>		



    def getCapabilities(self, data):
        logger.info("getCapabilities()")
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
        logger.info("getServices()")
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

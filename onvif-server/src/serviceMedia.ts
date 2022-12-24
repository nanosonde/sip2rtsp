import util from "util";
import { OnvifServer } from "./serverMockup";

export class MediaService {

	public readonly serviceName = "media";

	constructor(server: OnvifServer) {
		server.registerMethod(this.serviceName, 'getSnapshotUri', (args: any) => this.getSnapshotUri(args));
		server.registerMethod(this.serviceName, 'getVideoSources', (args: any) => this.getVideoSources(args));
		server.registerMethod(this.serviceName, 'getProfiles', (args: any) => this.getProfiles(args));
		server.registerMethod(this.serviceName, 'getProfile', (args: any) => this.getProfile(args));
		server.registerMethod(this.serviceName, 'getAudioSources', (args: any) => this.getAudioSources(args));
		server.registerMethod(this.serviceName, 'getStreamUri', (args: any) => this.getStreamUri(args));
		server.registerMethod(this.serviceName, 'getVideoSourceConfiguration', (args: any) => this.getVideoSourceConfiguration(args));
		server.registerMethod(this.serviceName, 'getVideoEncoderConfigurationOptions', (args: any) => this.getVideoEncoderConfigurationOptions(args));

		server.registerMethod(this.serviceName, 'setVideoEncoderConfiguration', (args: any) => this.setVideoEncoderConfiguration(args));
    }

	private getSnapshotUri(args: any): string {

		console.log("getSnapshotUri(): " + util.inspect(args, false, null, true));

		return `
			<trt:GetSnapshotUriResponse>
			  <trt:MediaUri>
				<tt:Uri>http://10.10.10.10:54321/snapshot</tt:Uri>
				<tt:InvalidAfterConnect>false</tt:InvalidAfterConnect>
				<tt:InvalidAfterReboot>false</tt:InvalidAfterReboot>
				<tt:Timeout>PT0S</tt:Timeout>
			  </trt:MediaUri>
			</trt:GetSnapshotUriResponse>
		`;
	}

    private getVideoSources(args: any): string {

		console.log("getVideoSources(): " + util.inspect(args, false, null, true));
		return `
            <trt:GetVideoSourcesResponse>
                <trt:VideoSources token="vidsrc0">
                    <tt:Framerate>30</tt:Framerate>
                    <tt:Resolution>
                        <tt:Width>1920</tt:Width>
                        <tt:Height>1080</tt:Height>
                    </tt:Resolution>
                </trt:VideoSources>
            </trt:GetVideoSourcesResponse>

		`;
	}

    private getProfiles(args: any): string {

		console.log("getProfiles(): " + util.inspect(args, false, null, true));
		return `
            <trt:GetProfilesResponse>
                <trt:Profiles fixed="true" token="main">
                    <tt:Name>main</tt:Name>
                    <tt:VideoSourceConfiguration token="vscfg0">
                        <tt:Name>vscfg0</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:SourceToken>vidsrc0</tt:SourceToken>
                        <tt:Bounds height="1080" width="1920" y="0" x="0"></tt:Bounds>
                    </tt:VideoSourceConfiguration>
                    <tt:VideoEncoderConfiguration token="main">
                        <tt:Name>Main stream encoder</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:Encoding>H264</tt:Encoding>
                        <tt:Resolution>
                            <tt:Width>1920</tt:Width>
                            <tt:Height>1080</tt:Height>
                        </tt:Resolution>
                        <tt:Quality>8</tt:Quality>
                        <tt:RateControl>
                            <tt:FrameRateLimit>5</tt:FrameRateLimit>
                            <tt:EncodingInterval>1</tt:EncodingInterval>
                            <tt:BitrateLimit>1000</tt:BitrateLimit>
                        </tt:RateControl>
                        <tt:H264>
                            <tt:GovLength>30</tt:GovLength>
                            <tt:H264Profile>High</tt:H264Profile>
                        </tt:H264>
                        <tt:Multicast>
                            <tt:Address>
                                <tt:Type>IPv4</tt:Type>
                                <tt:IPv4Address>0.0.0.0</tt:IPv4Address>
                            </tt:Address>
                            <tt:Port>0</tt:Port>
                            <tt:TTL>0</tt:TTL>
                            <tt:AutoStart>false</tt:AutoStart>
                        </tt:Multicast>
                        <tt:SessionTimeout>PT60S</tt:SessionTimeout>
                    </tt:VideoEncoderConfiguration>
                    <tt:PTZConfiguration token="default">
                        <tt:Name>default</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:NodeToken>default</tt:NodeToken>
                        <tt:DefaultAbsolutePantTiltPositionSpace>http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace</tt:DefaultAbsolutePantTiltPositionSpace>
                        <tt:DefaultAbsoluteZoomPositionSpace>http://www.onvif.org/ver10/tptz/ZoomSpaces/PositionGenericSpace</tt:DefaultAbsoluteZoomPositionSpace>
                        <tt:DefaultRelativePanTiltTranslationSpace>http://www.onvif.org/ver10/tptz/PanTiltSpaces/TranslationGenericSpace</tt:DefaultRelativePanTiltTranslationSpace>
                        <tt:DefaultRelativeZoomTranslationSpace>http://www.onvif.org/ver10/tptz/ZoomSpaces/TranslationGenericSpace</tt:DefaultRelativeZoomTranslationSpace>
                        <tt:DefaultContinuousPanTiltVelocitySpace>http://www.onvif.org/ver10/tptz/PanTiltSpaces/VelocityGenericSpace</tt:DefaultContinuousPanTiltVelocitySpace>
                        <tt:DefaultContinuousZoomVelocitySpace>http://www.onvif.org/ver10/tptz/ZoomSpaces/VelocityGenericSpace</tt:DefaultContinuousZoomVelocitySpace>
                        <tt:DefaultPTZSpeed>
                            <tt:PanTilt space="http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace" y="1" x="1"></tt:PanTilt>
                            <tt:Zoom space="http://www.onvif.org/ver10/tptz/ZoomSpaces/ZoomGenericSpeedSpace" x="1"></tt:Zoom>
                        </tt:DefaultPTZSpeed>
                        <tt:DefaultPTZTimeout>PT1093754.348S</tt:DefaultPTZTimeout>
                    </tt:PTZConfiguration>
                </trt:Profiles>
            </trt:GetProfilesResponse>        
		`;
	}

    private getProfile(args: any): string {

		console.log("getProfile(): " + util.inspect(args, false, null, true));
		return `
            <trt:GetProfileResponse>
                <trt:Profile token="main">
                    <tt:Name>ProfileName</tt:Name>
                    <tt:VideoSourceConfiguration token="video-source-config-token">
                        <tt:Name>VideoSourceConfigName</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:SourceToken>video-source-token</tt:SourceToken>
                    </tt:VideoSourceConfiguration>
                    <tt:AudioSourceConfiguration token="audio-source-config-token">
                        <tt:Name>AudioSourceConfigName</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:SourceToken>audio-source-token</tt:SourceToken>
                    </tt:AudioSourceConfiguration>
                    <tt:VideoEncoderConfiguration token="video-encoder-config-token">
                        <tt:Name>VideoEncoderConfigName</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:Encoding>H264</tt:Encoding>
                        <tt:Resolution>
                            <tt:Width>1920</tt:Width>
                            <tt:Height>1080</tt:Height>
                        </tt:Resolution>
                        <tt:Quality>1</tt:Quality>
                    </tt:VideoEncoderConfiguration>
                    <tt:AudioEncoderConfiguration token="audio-encoder-config-token">
                        <tt:Name>AudioEncoderConfigName</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:Encoding>AAC</tt:Encoding>
                        <tt:Bitrate>128000</tt:Bitrate>
                        <tt:SampleRate>44100</tt:SampleRate>
                    </tt:AudioEncoderConfiguration>
                    <tt:PTZConfiguration token="ptz-config-token">
                        <tt:Name>PTZConfigName</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                        <tt:NodeToken>ptz-node-token</tt:NodeToken>
                    </tt:PTZConfiguration>
                    <tt:MetadataConfiguration token="metadata-config-token">
                        <tt:Name>MetadataConfigName</tt:Name>
                        <tt:UseCount>1</tt:UseCount>
                    </tt:MetadataConfiguration>
                </trt:Profile>
            </trt:GetProfileResponse>
        `;
	}

    private getAudioSources(args: any): string {

		console.log("getAudioSources(): " + util.inspect(args, false, null, true));
		return `
            <trt:GetAudioSourcesResponse>
                <trt:AudioSources token="src0">
                </trt:AudioSources>
            </trt:GetAudioSourcesResponse>
		`;
	}

    private getStreamUri(args: any): string {
//                    <tt:Uri>rtsp://10.10.10.10:8554/hauseingang</tt:Uri>

		console.log("getStreamUri(): " + util.inspect(args, false, null, true));
		return `
            <trt:GetStreamUriResponse>
                <trt:MediaUri>
                    <tt:Uri>rtsp://10.10.10.70:8554/test</tt:Uri>
                    <tt:InvalidAfterConnect>false</tt:InvalidAfterConnect>
                    <tt:InvalidAfterReboot>false</tt:InvalidAfterReboot>
                    <tt:Timeout>PT0S</tt:Timeout>
                </trt:MediaUri>
            </trt:GetStreamUriResponse>
		`;
	}

    private getVideoSourceConfiguration(args: any): string {

		console.log("getVideoSourceConfiguration(): " + util.inspect(args, false, null, true));
		return `
            <trt:GetVideoSourceConfigurationResponse>
            </trt:GetVideoSourceConfigurationResponse>
		`;
	}

    private getVideoEncoderConfigurationOptions(args: any): string {

		console.log("getVideoEncoderConfigurationOptions(): " + util.inspect(args, false, null, true));
		return `
            <trt:GetVideoEncoderConfigurationOptionsResponse>
                <trt:Options>
                    <tt:QualityRange>
                            <tt:Min>1</tt:Min>
                            <tt:Max>100</tt:Max>
                    </tt:QualityRange>
                    <tt:JPEG>
                            <tt:FrameRateRange>
                                    <tt:Min>5</tt:Min>
                                    <tt:Max>25</tt:Max>
                            </tt:FrameRateRange>
                            <tt:EncodingIntervalRange>
                                    <tt:Min>1</tt:Min>
                                    <tt:Max>1</tt:Max>
                            </tt:EncodingIntervalRange>
                    </tt:JPEG>
                    <tt:MPEG4>
                            <tt:ResolutionsAvailable>
                                    <tt:Width>1920</tt:Width>
                                    <tt:Height>1080</tt:Height>
                            </tt:ResolutionsAvailable>
                            <tt:ResolutionsAvailable>
                                    <tt:Width>1280</tt:Width>
                                    <tt:Height>720</tt:Height>
                            </tt:ResolutionsAvailable>
                            <tt:ResolutionsAvailable>
                                    <tt:Width>720</tt:Width>
                                    <tt:Height>576</tt:Height>
                            </tt:ResolutionsAvailable>
                            <tt:GovLengthRange>
                                    <tt:Min>1</tt:Min>
                                    <tt:Max>25</tt:Max>
                            </tt:GovLengthRange>
                            <tt:FrameRateRange>
                                    <tt:Min>5</tt:Min>
                                    <tt:Max>25</tt:Max>
                            </tt:FrameRateRange>
                            <tt:EncodingIntervalRange>
                                    <tt:Min>1</tt:Min>
                                    <tt:Max>1</tt:Max>
                            </tt:EncodingIntervalRange>
                            <tt:Mpeg4ProfilesSupported>SP</tt:Mpeg4ProfilesSupported>
                    </tt:MPEG4>
                    <tt:H264>
                            <tt:ResolutionsAvailable>
                                    <tt:Width>1920</tt:Width>
                                    <tt:Height>1080</tt:Height>
                            </tt:ResolutionsAvailable>
                            <tt:ResolutionsAvailable>
                                    <tt:Width>1280</tt:Width>
                                    <tt:Height>720</tt:Height>
                            </tt:ResolutionsAvailable>
                            <tt:ResolutionsAvailable>
                                    <tt:Width>720</tt:Width>
                                    <tt:Height>576</tt:Height>
                            </tt:ResolutionsAvailable>
                            <tt:GovLengthRange>
                                    <tt:Min>1</tt:Min>
                                    <tt:Max>25</tt:Max>
                            </tt:GovLengthRange>
                            <tt:FrameRateRange>
                                    <tt:Min>5</tt:Min>
                                    <tt:Max>25</tt:Max>
                            </tt:FrameRateRange>
                            <tt:EncodingIntervalRange>
                                    <tt:Min>1</tt:Min>
                                    <tt:Max>1</tt:Max>
                            </tt:EncodingIntervalRange>
                            <tt:H264ProfilesSupported>High</tt:H264ProfilesSupported>
                    </tt:H264>
                </trt:Options>
            </trt:GetVideoEncoderConfigurationOptionsResponse>
		`;
	}

    private setVideoEncoderConfiguration(args: any): string {

		console.log("setVideoEncoderConfiguration(): " + util.inspect(args, false, null, true));
		return `
            <trt:SetVideoEncoderConfigurationResponse></trt:SetVideoEncoderConfigurationResponse>
		`;
	}
}

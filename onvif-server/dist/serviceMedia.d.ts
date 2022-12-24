import { OnvifServer } from "./serverMockup";
export declare class MediaService {
    readonly serviceName = "media";
    constructor(server: OnvifServer);
    private getSnapshotUri;
    private getVideoSources;
    private getProfiles;
    private getProfile;
    private getAudioSources;
    private getStreamUri;
    private getVideoSourceConfiguration;
    private getVideoEncoderConfigurationOptions;
    private setVideoEncoderConfiguration;
}

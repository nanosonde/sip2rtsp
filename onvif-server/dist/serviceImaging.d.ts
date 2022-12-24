import { OnvifServer } from "./serverMockup";
export declare class ImagingService {
    readonly serviceName = "imaging";
    constructor(server: OnvifServer);
    private getImagingSettings;
    private getMoveOptions;
    private getOptions;
    private setImagingSettings;
}

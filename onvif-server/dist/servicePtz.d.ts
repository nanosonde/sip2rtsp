import { OnvifServer } from "./serverMockup";
export declare class PtzService {
    readonly serviceName = "ptz";
    constructor(server: OnvifServer);
    private getPresets;
    private getNodes;
    private gotoPreset;
    private gotoHomePosition;
}

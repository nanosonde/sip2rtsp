"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ImagingService = void 0;
const util_1 = __importDefault(require("util"));
class ImagingService {
    constructor(server) {
        this.serviceName = "imaging";
        server.registerMethod(this.serviceName, 'getImagingSettings', (args) => this.getImagingSettings(args));
        server.registerMethod(this.serviceName, 'getMoveOptions', (args) => this.getMoveOptions(args));
        server.registerMethod(this.serviceName, 'getOptions', (args) => this.getOptions(args));
        server.registerMethod(this.serviceName, 'setImagingSettings', (args) => this.setImagingSettings(args));
    }
    getImagingSettings(args) {
        console.log("getImagingSettings(): " + util_1.default.inspect(args, false, null, true));
        return `
            <timg:GetImagingSettingsResponse>
                <timg:ImagingSettings>
                    <tt:Brightness>255</tt:Brightness>
                    <tt:ColorSaturation>128</tt:ColorSaturation>
                    <tt:Contrast>128</tt:Contrast>
                    <tt:Focus>
                        <tt:AutoFocusMode>AUTO</tt:AutoFocusMode>
                    </tt:Focus>
                    <tt:Sharpness>128</tt:Sharpness>
                </timg:ImagingSettings>
            </timg:GetImagingSettingsResponse>
		`;
    }
    getMoveOptions(args) {
        console.log("getMoveOptions(): " + util_1.default.inspect(args, false, null, true));
        return `
            <timg:GetMoveOptionsResponse></timg:GetMoveOptionsResponse>
		`;
    }
    getOptions(args) {
        console.log("getOptions(): " + util_1.default.inspect(args, false, null, true));
        return `
            <timg:GetOptionsResponse>
                <timg:ImagingOptions>
                    <tt:Brightness>
                        <tt:Min>0.00</tt:Min>
                        <tt:Max>255.00</tt:Max>
                    </tt:Brightness>
                    <tt:ColorSaturation>
                        <tt:Min>0.00</tt:Min>
                        <tt:Max>255.00</tt:Max>
                    </tt:ColorSaturation>
                    <tt:Contrast>
                        <tt:Min>0.00</tt:Min>
                        <tt:Max>255.00</tt:Max>
                    </tt:Contrast>
                </timg:ImagingOptions>
            </timg:GetOptionsResponse>
		`;
    }
    setImagingSettings(args) {
        console.log("setImagingSettings(): " + util_1.default.inspect(args, false, null, true));
        return `
            <timg:SetImagingSettingsResponse></timg:SetImagingSettingsResponse>
		`;
    }
}
exports.ImagingService = ImagingService;
//# sourceMappingURL=serviceImaging.js.map
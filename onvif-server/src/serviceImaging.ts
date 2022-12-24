import util from "util";
import { OnvifServer } from "./serverMockup";

export class ImagingService {

	public readonly serviceName = "imaging";

	constructor(server: OnvifServer) {
		server.registerMethod(this.serviceName, 'getImagingSettings', (args: any) => this.getImagingSettings(args));
		server.registerMethod(this.serviceName, 'getMoveOptions', (args: any) => this.getMoveOptions(args));
		server.registerMethod(this.serviceName, 'getOptions', (args: any) => this.getOptions(args));

		server.registerMethod(this.serviceName, 'setImagingSettings', (args: any) => this.setImagingSettings(args));
    }

	private getImagingSettings(args: any): string {

		console.log("getImagingSettings(): " + util.inspect(args, false, null, true));

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

    private getMoveOptions(args: any): string {

		console.log("getMoveOptions(): " + util.inspect(args, false, null, true));

		return `
            <timg:GetMoveOptionsResponse></timg:GetMoveOptionsResponse>
		`;
	}

    private getOptions(args: any): string {

		console.log("getOptions(): " + util.inspect(args, false, null, true));

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

    private setImagingSettings(args: any): string {

		console.log("setImagingSettings(): " + util.inspect(args, false, null, true));

		return `
            <timg:SetImagingSettingsResponse></timg:SetImagingSettingsResponse>
		`;
	}

}

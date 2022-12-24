"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PtzService = void 0;
const util_1 = __importDefault(require("util"));
class PtzService {
    constructor(server) {
        this.serviceName = "ptz";
        server.registerMethod(this.serviceName, 'getPresets', (args) => this.getPresets(args));
        server.registerMethod(this.serviceName, 'getNodes', (args) => this.getNodes(args));
        server.registerMethod(this.serviceName, 'gotoPreset', (args) => this.gotoPreset(args));
        server.registerMethod(this.serviceName, 'gotoHomePosition', (args) => this.gotoHomePosition(args));
    }
    getPresets(args) {
        console.log("getPresets(): " + util_1.default.inspect(args, false, null, true));
        return `
            <tptz:GetPresetsResponse>
                <tptz:Preset token="P001">
                    <tt:Name>P001</tt:Name>
                </tptz:Preset>
                {{? !it.one }}
                <tptz:Preset token="P002">
                    <tt:Name>P002</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P003">
                    <tt:Name>P003</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P004">
                    <tt:Name>P004</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P005">
                    <tt:Name>P005</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P006">
                    <tt:Name>P006</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P007">
                    <tt:Name>P007</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P008">
                    <tt:Name>P008</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P009">
                    <tt:Name>P009</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P010">
                    <tt:Name>P010</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P011">
                    <tt:Name>P011</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P012">
                    <tt:Name>P012</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P013">
                    <tt:Name>P013</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P014">
                    <tt:Name>P014</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P015">
                    <tt:Name>P015</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P016">
                    <tt:Name>P016</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P017">
                    <tt:Name>P017</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P018">
                    <tt:Name>P018</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P019">
                    <tt:Name>P019</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="P020">
                    <tt:Name>P020</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DarkAutoIROn">
                    <tt:Name>DarkAutoIROn</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DarkAutoWhiteOn">
                    <tt:Name>DarkAutoWhiteOn</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DarkAutoLightsOff">
                    <tt:Name>DarkAutoLightsOff</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DarkAutoMono">
                    <tt:Name>DarkAutoMono</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DarkAutoColour">
                    <tt:Name>DarkAutoColour</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DarkAutoFocusWhite">
                    <tt:Name>DarkAutoFocusWhite</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DarkAutoFocusIR">
                    <tt:Name>DarkAutoFocusIR</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DoubleWipe">
                    <tt:Name>DoubleWipe</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="PermanentIntermittentWipe">
                    <tt:Name>PermanentIntermittentWipe</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="PermanentFastWipe">
                    <tt:Name>PermanentFastWipe</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="TimedIntermittentWipe">
                    <tt:Name>TimedIntermittentWipe</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="TimedFastWipe">
                    <tt:Name>TimedFastWipe</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WipeOff">
                    <tt:Name>WipeOff</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DeFogOn">
                    <tt:Name>DeFogOn</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="DeFogOff">
                    <tt:Name>DeFogOff</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WasherOn">
                    <tt:Name>WasherOn</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WasherOff">
                    <tt:Name>WasherOff</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="ForceWhiteLightsOn">
                    <tt:Name>ForceWhiteLightsOn</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="ForceWhiteLightsOff">
                    <tt:Name>ForceWhiteLightsOff</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WhiteLightsOn">
                    <tt:Name>WhiteLightsOn</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WhiteLightsOff">
                    <tt:Name>WhiteLightsOff</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WhiteExclusionLeft">
                    <tt:Name>WhiteExclusionLeft</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WhiteExclusionRight">
                    <tt:Name>WhiteExclusionRight</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="WasherPosition">
                    <tt:Name>WasherPosition</tt:Name>
                </tptz:Preset>
                <tptz:Preset token="Home">
                    <tt:Name>Home</tt:Name>
                </tptz:Preset>
            </tptz:GetPresetsResponse>
		`;
    }
    getNodes(args) {
        console.log("getNodes(): " + util_1.default.inspect(args, false, null, true));
        return `
            <tptz:GetNodesResponse>
                <tptz:PTZNode token="default">
                    <tt:Name>default</tt:Name>
                    <tt:SupportedPTZSpaces>
                        <tt:AbsolutePanTiltPositionSpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>0</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                            <tt:YRange>
                                <tt:Min>0</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:YRange>
                        </tt:AbsolutePanTiltPositionSpace>
                        <tt:AbsoluteZoomPositionSpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/ZoomSpaces/PositionGenericSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>0</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                        </tt:AbsoluteZoomPositionSpace>
                        <tt:RelativePanTiltTranslationSpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/PanTiltSpaces/TranslationGenericSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>-1</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                            <tt:YRange>
                                <tt:Min>-1</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:YRange>
                        </tt:RelativePanTiltTranslationSpace>
                        <tt:RelativeZoomTranslationSpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/ZoomSpaces/TranslationGenericSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>-1</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                        </tt:RelativeZoomTranslationSpace>
                        <tt:ContinuousPanTiltVelocitySpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/PanTiltSpaces/VelocityGenericSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>-1</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                            <tt:YRange>
                                <tt:Min>-1</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:YRange>
                        </tt:ContinuousPanTiltVelocitySpace>
                        <tt:ContinuousZoomVelocitySpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/ZoomSpaces/VelocityGenericSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>-1</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                        </tt:ContinuousZoomVelocitySpace>
                        <tt:PanTiltSpeedSpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>0</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                        </tt:PanTiltSpeedSpace>
                        <tt:ZoomSpeedSpace>
                            <tt:URI>http://www.onvif.org/ver10/tptz/ZoomSpaces/ZoomGenericSpeedSpace</tt:URI>
                            <tt:XRange>
                                <tt:Min>0</tt:Min>
                                <tt:Max>1</tt:Max>
                            </tt:XRange>
                        </tt:ZoomSpeedSpace>
                    </tt:SupportedPTZSpaces>
                    <tt:MaximumNumberOfPresets>360</tt:MaximumNumberOfPresets>
                    <tt:HomeSupported>true</tt:HomeSupported>
                    <tt:AuxiliaryCommands>AUX1</tt:AuxiliaryCommands>
                    <tt:AuxiliaryCommands>AUX2</tt:AuxiliaryCommands>
                    <tt:AuxiliaryCommands>AUX3</tt:AuxiliaryCommands>
                    <tt:AuxiliaryCommands>AUX4</tt:AuxiliaryCommands>
                    <tt:AuxiliaryCommands>AUX5</tt:AuxiliaryCommands>
                    <tt:AuxiliaryCommands>AUX6</tt:AuxiliaryCommands>
                    <tt:AuxiliaryCommands>AUX7</tt:AuxiliaryCommands>
                    <tt:AuxiliaryCommands>AUX8</tt:AuxiliaryCommands>
                </tptz:PTZNode>
            </tptz:GetNodesResponse>        
		`;
    }
    gotoPreset(args) {
        console.log("gotoPreset(): " + util_1.default.inspect(args, false, null, true));
        return `
            <tptz:GotoPresetResponse></tptz:GotoPresetResponse>
		`;
    }
    gotoHomePosition(args) {
        console.log("gotoHomePosition(): " + util_1.default.inspect(args, false, null, true));
        return `
            <tptz:GotoHomePositionResponse></tptz:GotoHomePositionResponse>
		`;
    }
}
exports.PtzService = PtzService;
//# sourceMappingURL=servicePtz.js.map
import logging
from pyonvifsrv.context import Context

logger = logging.getLogger(__name__)

class ImagingService:
    def __init__(self, context: Context):
        self.context = context

    def getImagingSettings(self, data):
        return '''
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
        '''

    def getMoveOptions(self, data):
        return '''
            <timg:GetMoveOptionsResponse></timg:GetMoveOptionsResponse>
        '''
    def getOptions(self, data):
        return '''
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
        '''

    def setImagingSettings(self, data):
        return '''
            <timg:SetImagingSettingsResponse></timg:SetImagingSettingsResponse>
        '''

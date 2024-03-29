import logging

logger = logging.getLogger(__name__)

class Context:
    
    def __init__(self, config):
        self.firmwareVersion = "N/A"
        self.config = config
        self.services = []

        self.interfaceName = "ens3"
        self.hostName = self.config.onvif.hostname
        self.hostIP = self.config.onvif.advertised_server_address
        self.hostPort = self.config.onvif.advertised_server_port

        self.hostUrl = "http://" + self.hostIP + ":" + str(self.hostPort)

        self.baseServicePath = "/onvif/service"
        self.baseServiceAddress = self.hostUrl + self.baseServicePath
        self.serviceAddresses = {
            "device": self.baseServiceAddress + "/device",
            "media": self.baseServiceAddress + "/media",
            "imaging": self.baseServiceAddress + "/imaging",
            "events": self.baseServiceAddress + "/events",
            "ptz": self.baseServiceAddress + "/ptz",
            "deviceio": self.baseServiceAddress + "/deviceio",
        }

        self.cameraName = self.config.onvif.camera.name
        self.cameraLocation = self.config.onvif.camera.location
        self.cameraWidth = self.config.onvif.camera.width
        self.cameraHeight = self.config.onvif.camera.height
        self.cameraFps = self.config.onvif.camera.fps
        self.cameraBitrate = self.config.onvif.camera.bitrate

        self.snapshotUri = self.config.onvif.camera.snapshotUri
        self.streamUri = self.config.onvif.camera.streamUri


    def getService(self, serviceName):
        for service in self.services:
            if service.serviceName == serviceName:
                return service
        return None
  
    def triggerDoorbellEvent(self):
        logger.info("Triggering doorbell event on topic {topic}".format(topic = self.config.onvif.camera.eventTopicDoorbell))
        eventsService = self.getService("events")
        eventsService.triggerEvent(self.config.onvif.camera.eventTopicDoorbell, {'source_value': '000', 'state_value': 'true'})
        eventsService.triggerEvent(self.config.onvif.camera.eventTopicDoorbell, {'source_value': '000', 'state_value': 'false'})

    def setFirmwareVersion(self, firmwareVersion):
        self.firmwareVersion = firmwareVersion

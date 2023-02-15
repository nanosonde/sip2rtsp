import logging

logger = logging.getLogger(__name__)

class Context:
    
    snaphotUri = "http://10.10.10.10:54321/snapshot"
    streamUri = "rtsp://10.10.10.70:8554/test"

    def __init__(self, config):
        self.config = config
        self.services = []

        self.hostIP = self.config.onvif.server_address
        self.hostPort = self.config.onvif.server_port

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


    def getService(self, serviceName):
        for service in self.services:
            if service.serviceName == serviceName:
                return service
        return None
  
    def triggerDoorbellEvent(self):
        logger.info("Triggering doorbell event")
        eventsService = self.getService("events")
        eventsService.triggerEvent('tns1:Device/tnsaxis:VideoSource/tnsaxis:MotionAlarm', {'device': 'device1', 'type': 'motion', 'data': 'true'})




class Context:
    hostIP = "10.10.10.70"
    hostPort = 10101
    hostUrl = "http://" + hostIP + ":" + str(hostPort)

    baseServicePath = "/onvif/service"
    baseServiceAddress = hostUrl + baseServicePath
    serviceAddresses = {
        "device": baseServiceAddress + "/device",
        "media": baseServiceAddress + "/media",
        "imaging": baseServiceAddress + "/imaging",
        "events": baseServiceAddress + "/events",
        "ptz": baseServiceAddress + "/ptz",
        "deviceio": baseServiceAddress + "/deviceio",
    }

    snaphotUri = "http://10.10.10.10:54321/snapshot"
    streamUri = "rtsp://10.10.10.70:8554/test"

    def __init__(self, config):
        self.config = config


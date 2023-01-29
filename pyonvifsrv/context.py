


class Context:
    serviceAddress = "http://10.10.10.70:10101/onvif/services"
    snaphotUri = "http://10.10.10.10:54321/snapshot"
    streamUri = "rtsp://10.10.10.70:8554/test"

    def __init__(self, config):
        self.config = config



import logging
from tornado.web import Application, RequestHandler

from pyonvifsrv.context import Context
from pyonvifsrv.service_device import DeviceService
from pyonvifsrv.service_media import MediaService
from pyonvifsrv.service_imaging import ImagingService
from pyonvifsrv.service_events import EventsService
from pyonvifsrv.service_ptz import PtzService

logger = logging.getLogger(__name__)

class OnvifServer:
    def __init__(self, loop, config) -> None:
        self.loop = loop
        self.config = config
        self.context = Context(config)
        self.services = [
            DeviceService(self.context),
            MediaService(self.context),
            ImagingService(self.context),
            EventsService(self.context),
            PtzService(self.context),
        ]

    class _MainHandler(RequestHandler):
        def get(self):
            logger.info(self.request)
            self.write("Hello, world")
            self.finish()

    async def start_server(self):
        logger.info("ONVIF server starting...")

        handlers = [(r"/", self._MainHandler)]

        for service in self.services:
            handlers.append(service.getRequestHandler())

        app = Application(handlers)
        app.listen(10101)

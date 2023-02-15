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
        self.context.services = self.services
        logging.getLogger("tornado.access").setLevel(logging.WARNING)
        logging.getLogger("tornado.application").setLevel(logging.INFO)
        logging.getLogger("tornado.general").setLevel(logging.INFO)

    def getContext(self) -> Context:
        return self.context

    class _MainHandler(RequestHandler):
        def get(self):
            logger.info(self.request)
            self.write("Hello, world")
            self.finish()

    async def start_server(self):
        logger.info("ONVIF server starting...")

        handlers = [(r"/", self._MainHandler)]

        default_handler_class = None
        for service in self.services:
            # The device service is the default handler if no other path matches
            if service.serviceName == "device":
                default_handler_class = service._ServiceHandler
                default_handler_args = dict(serviceInstance=service)
            handlers += service.getRequestHandler()

        app = Application(
            handlers,
            default_handler_class=default_handler_class,
            default_handler_args=default_handler_args,
        )
        app.listen(port = self.config.onvif.server_port, address = self.config.onvif.server_address)

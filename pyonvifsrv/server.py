
import json
import logging
from tornado.web import Application, RequestHandler
import tornado.platform.asyncio

from pyonvifsrv.utils import parseSOAPString

logger = logging.getLogger(__name__)

class OnvifServer:
    def __init__(self, loop) -> None:
        self.loop = loop
        # Initialize the Tornado IOLoop with the asyncio event loop
        tornado.platform.asyncio.AsyncIOMainLoop().install()

    class MainHandler(RequestHandler):
        def get(self):
            logger.info(self.request)
        def post(self):
            httpBody = self.request.body.decode('utf-8')
            logger.info(f"HTTP body: {httpBody}")
            [data, rawXml] = parseSOAPString(httpBody)
            logging.info(f"data: \n{json.dumps(data, indent=4)}")


            self.set_header("Content-Type", "application/soap+xml; charset=utf-8")
            self.write(rawXml)

    async def start_server(self):
        logger.info("ONVIF server starting...")
        app = Application([(r"/onvif/device_service", self.MainHandler)])
        app.listen(10101)

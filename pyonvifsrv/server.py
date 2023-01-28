
import json
import logging
from tornado.web import Application, RequestHandler

from pyonvifsrv.utils import parseSOAPString

logger = logging.getLogger(__name__)

class OnvifServer:
    def __init__(self, loop, config) -> None:
        self.loop = loop
        self.config = config

    class _MainHandler(RequestHandler):
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
        app = Application([(r"/onvif/device_service", self._MainHandler)])
        app.listen(10101)

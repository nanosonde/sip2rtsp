
import json
import logging
from tornado.web import Application, RequestHandler

from pyonvifsrv.utils import parseSOAPString, getServiceNameFromOnvifNS, getMethodNameFromBody, decapitalize, envelopeHeader, envelopeFooter

from pyonvifsrv.context import Context
from pyonvifsrv.service_device import DeviceService

logger = logging.getLogger(__name__)

class OnvifServer:
    def __init__(self, loop, config) -> None:
        self.loop = loop
        self.config = config
        self.context = Context(config)
        self.services = { 
            "device": DeviceService(self.context)
        }

    class _MainHandler(RequestHandler):
        def initialize(self, services):
            self.services = services
        def get(self):
            logger.info(self.request)
        def post(self):
            httpBody = self.request.body.decode('utf-8')
            #logger.debug(f"HTTP request body: {httpBody}")

            # Parse the SOAP XML and create a dictionary which contains the
            # SOAP header and body
            data = parseSOAPString(httpBody)
            logging.info(f"data: \n{json.dumps(data, indent=4)}")

            serviceName = getServiceNameFromOnvifNS(data["body"]["$NS"])
            logging.info(f"serviceName: {serviceName}")

            responseBody = ""
            serviceInstance = self.services[serviceName]
            methodName = decapitalize(getMethodNameFromBody(data["body"]))
            if methodName:
                method = getattr(serviceInstance, methodName)
                responseBody = method(data)

            if responseBody:
                self.set_header("Content-Type", "application/soap+xml; charset=utf-8")
                content = envelopeHeader(data["header"]) + responseBody + envelopeFooter();
                logger.debug(f"HTTP response body: {content}")
                self.write(content)
                self.flush()

    async def start_server(self):
        logger.info("ONVIF server starting...")
        app = Application([(r"/onvif/device_service", self._MainHandler, dict(services=self.services))])
        app.listen(10101)

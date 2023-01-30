
import json
import logging
from tornado.web import Application, RequestHandler

from pyonvifsrv.utils import parseSOAPString, getServiceNameFromOnvifNS, getMethodNameFromBody, decapitalize, envelopeHeader, envelopeFooter

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
        def initialize(self, services):
            self.services = services
        def get(self):
            logger.info(self.request)
        def post(self, serviceName):
            reqBody = self.request.body.decode('utf-8')
            #logger.debug(f"HTTP request body: {httpBody}")

            # Parse the SOAP XML and create a dictionary which contains the
            # SOAP header and body
            reqData = parseSOAPString(reqBody)
            logging.info(f"data: \n{json.dumps(reqData, indent=4)}")

            #serviceName = getServiceNameFromOnvifNS(reqData["body"]["$NS"])
            logging.info(f"serviceName: {serviceName}")

            responseBody = ""

            serviceInstance = None
            for service in self.services:
                if service.serviceName == serviceName:
                    serviceInstance = service
                    break

            if serviceInstance is None:
                logger.error(f"Service {serviceName} not found")
                self.set_status(500)
                self.finish()
                return

            #serviceInstance = self.services[serviceName]
            methodName = decapitalize(getMethodNameFromBody(reqData["body"]))
            if methodName:
                try:
                    method = getattr(serviceInstance, methodName)
                except AttributeError:
                    logger.error(f"Method {methodName} not found in service {serviceName}")
                    self.set_status(500)
                    self.finish()
                    return
                responseBody = method(reqData)
            else:
                logger.error("No method name found in request data: {data}".format(data=reqData["body"]))
                self.set_status(500)
                self.finish()
                return

            if responseBody != "":
                self.set_header("Content-Type", "application/soap+xml; charset=utf-8")
                content = envelopeHeader(reqData["header"]) + responseBody + envelopeFooter();
                #logger.debug(f"HTTP response body: {content}")
                self.write(content)
                self.finish()
            else:
                logger.error("No response body was generated")
                self.set_status(500)
                self.finish()

    async def start_server(self):
        logger.info("ONVIF server starting...")

        app = Application([(r"/onvif/service/([a-z]+)", self._MainHandler, dict(services=self.services))])
        app.listen(10101)

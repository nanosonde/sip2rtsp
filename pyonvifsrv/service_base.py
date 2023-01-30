import json
import logging

from tornado.web import RequestHandler

from pyonvifsrv.utils import parseSOAPString, getServiceNameFromOnvifNS, getMethodNameFromBody, decapitalize, envelopeHeader, envelopeFooter
from pyonvifsrv.context import Context

logger = logging.getLogger(__name__)

class ServiceBase:
    def __init__(self, context: Context):
        self.context = context

    def getRequestHandler(self):
        return (r"/onvif/service/" + self.serviceName, self._ServiceHandler, dict(serviceInstance=self))

    class _ServiceHandler(RequestHandler):
        def initialize(self, serviceInstance):
                self.serviceInstance = serviceInstance        
        def post(self):
            reqBody = self.request.body.decode('utf-8')
            #logger.debug(f"HTTP request body: {httpBody}")

            # Parse the SOAP XML and create a dictionary which contains the
            # SOAP header and body
            reqData = parseSOAPString(reqBody)
            logging.info(f"data: \n{json.dumps(reqData, indent=4)}")

            responseBody = ""

            methodName = decapitalize(getMethodNameFromBody(reqData["body"]))
            if methodName:
                try:
                    method = getattr(self.serviceInstance, methodName)
                except AttributeError:
                    logger.error(f"Method {methodName} not found in service {self.serviceInstance.serviceName}")
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


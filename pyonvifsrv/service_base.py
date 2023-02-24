import asyncio
import json
import logging
from typing import Tuple

from tornado.web import RequestHandler

from pyonvifsrv.utils import (
    parseSOAPString,
    getServiceNameFromOnvifNS,
    getMethodNameFromBody,
    decapitalize,
    envelopeHeader,
    envelopeFooter,
)
from pyonvifsrv.context import Context

logger = logging.getLogger(__name__)


class ServiceBase:
    # Override this in the derived class
    serviceName = None

    def __init__(self, context: Context):
        self.context = context

    def getRequestHandler(self):
        return [
            (
                r"/onvif/service/" + self.serviceName,
                self._ServiceHandler,
                dict(serviceInstance=self),
            )
        ]

    class _ServiceHandler(RequestHandler):
        def initialize(self, serviceInstance):
            self.serviceInstance = serviceInstance

        async def post(self):
            reqBody = self.request.body.decode("utf-8")
            # logger.debug(f"HTTP request body: {reqBody}")

            # Parse the SOAP XML and create a dictionary which contains the
            # SOAP header and body
            reqData = parseSOAPString(reqBody)
            # logging.debug(f"data: \n{json.dumps(reqData, indent=4)}")

            [responseCode, response] = await self.callMethodFromSoapRequestData(reqData)
            self.set_status(responseCode)
            self.write(response)
            self.finish()

        async def callMethodFromSoapRequestData(self, reqData) -> Tuple[int, str]:
            responseBody = ""

            methodName = decapitalize(getMethodNameFromBody(reqData["body"]))
            if methodName:
                try:
                    method = getattr(self.serviceInstance, methodName)
                except AttributeError:
                    logger.error(
                        f"Method {methodName} not found in service {self.serviceInstance.serviceName}"
                    )
                    return (500, responseBody)

                # Now call the method in the current class instance which generates the response
                if asyncio.iscoroutinefunction(method):
                    responseBody = await method(reqData)
                else:
                    responseBody = method(reqData)
            else:
                logger.error(
                    "No method name found in request data: {data}".format(
                        data=reqData["body"]
                    )
                )
                return (500, responseBody)

            if responseBody != "":
                self.set_header("Content-Type", "application/soap+xml; charset=utf-8")
                content = (
                    envelopeHeader(reqData["header"]) + responseBody + envelopeFooter()
                )
                # logger.debug(f"HTTP response body: {content}")
                httpStatusCode = 500 if "<SOAP-ENV:Fault>" in responseBody else 200
                return (httpStatusCode, content)
            else:
                logger.error(
                    "No response body was generated for method {methodName}".format(
                        methodName=methodName
                    )
                )
                return (500, responseBody)

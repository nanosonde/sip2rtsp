import re
import json
import time
import struct
import base64
import random
import asyncio
import hashlib
import logging
import datetime
import xml.etree.ElementTree as ET
from pprint import pformat, pprint
from typing import Tuple, Dict
from collections import defaultdict

import tornado.platform.asyncio
from tornado.web import Application, RequestHandler

logger = logging.getLogger(__name__)

def getNSAndTag(s):
    match = re.search(r"\{(.*)\}(.*)", s)
    if match:
        if match.group(1) == "":
            return None, match.group(2)
        else:
            return match.group(1), match.group(2)
    else:
        return None, s

def etree_to_dict(t):
    [ns, tagname] = getNSAndTag(t.tag)
    d = {}
    d["$NS"] = ns
    d[tagname] = {} if t.attrib else None
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {}
        d["$NS"] = ns
        d[tagname] = {k:v[0] if len(v) == 1 else v for k, v in dd.items()}
        #d = {tagname: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[tagname].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[tagname]['#text'] = text
        else:
            d[tagname] = text
    return d

def parseSOAPString(rawXml: str) -> Tuple[Dict[str, any], str]:
    
    root = ET.fromstring(rawXml)

    # Envelope element is already the root element
    body_element = root.find('./{http://www.w3.org/2003/05/soap-envelope}Body')
    if  body_element is None:
        raise ValueError('Invalid ONVIF SOAP envelope: no Body element found')

    if len(body_element) > 1:
        raise ValueError('Invalid ONVIF SOAP envelope: more than element found in Body')

    # Use the first and only element in the body
    first_element = body_element[0]
    if first_element is None:
        raise ValueError('Invalid ONVIF SOAP envelope: no valid element found in Body')

    for elem in first_element.iter():
        tag = elem.tag
        [ns, tagname] = getNSAndTag(tag)
        logger.info(f"elem: ns: {ns} tag: {tagname} - attrib: {elem.attrib}")

    myDict = etree_to_dict(first_element)
    return [myDict, rawXml]


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


async def start_server():
    app = Application([(r"/onvif/device_service", MainHandler)])
    app.listen(10101)


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s] %(name)-25s %(levelname)-8s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )

    # Initialize the Tornado IOLoop with the asyncio event loop
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())
    loop.run_forever()

def envelopeHeader(requestHeader):
    header = '''
    <?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope 
            xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" 
            xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" 
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex"
            xmlns:wsa5="http://www.w3.org/2005/08/addressing"
            xmlns:c14n="http://www.w3.org/2001/10/xml-exc-c14n#"
            xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
            xmlns:xenc="http://www.w3.org/2001/04/xmlenc#"
            xmlns:wsc="http://schemas.xmlsoap.org/ws/2005/02/sc"
            xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
            xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
            xmlns:xmime5="http://www.w3.org/2005/05/xmlmime"
            xmlns:xmime="http://tempuri.org/xmime.xsd"
            xmlns:xop="http://www.w3.org/2004/08/xop/include"
            xmlns:tt="http://www.onvif.org/ver10/schema"
            xmlns:wsrfbf="http://docs.oasis-open.org/wsrf/bf-2"
            xmlns:wstop="http://docs.oasis-open.org/wsn/t-1"
            xmlns:wsrfr="http://docs.oasis-open.org/wsrf/r-2"
            xmlns:tds="http://www.onvif.org/ver10/device/wsdl"
            xmlns:tev="http://www.onvif.org/ver10/events/wsdl"
            xmlns:wsnt="http://docs.oasis-open.org/wsn/b-2"
            xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl"
            xmlns:trt="http://www.onvif.org/ver10/media/wsdl"
            xmlns:timg="http://www.onvif.org/ver20/imaging/wsdl"
            xmlns:tmd="http://www.onvif.org/ver10/deviceIO/wsdl"
            xmlns:tns1="http://www.onvif.org/ver10/topics"
            xmlns:ter="http://www.onvif.org/ver10/error"
            xmlns:tnsaxis="http://www.axis.com/2009/event/topics">
    '''

    if requestHeader is not None:
        header += '<SOAP-ENV:Header>'

        if (requestHeader.messageID is not None):
            header += '<wsa5:MessageID>' + requestHeader.messageID + '</wsa5:MessageID>'

        if requestHeader.replyTo is not None:
            header += '<wsa5:ReplyTo SOAP-ENV:mustUnderstand="1">' + '<wsa5:Address>' + requestHeader.replyTo.address + '</wsa5:Address>' + '</wsa5:ReplyTo>'
    
        if requestHeader.to is not None:
            header += "<wsa5:To SOAP-ENV:mustUnderstand=\"1\">" + requestHeader.to._ + "</wsa5:To>"

        if requestHeader.action is not None:
            header += "<wsa5:Action SOAP-ENV:mustUnderstand=\"1\">" + requestHeader.action._.replace("Request$", "Response") + "</wsa5:Action>"
        
        if requestHeader.security is not None:  
            header += '<wsse:Security>'
            + '<wsse:UsernameToken>' 
            + "<wsse:Username>" + requestHeader.security.usernameToken.username + "</wsse:Username>"
            + "<wsse:Password Type=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest\">" + requestHeader.security.usernameToken.password._ + "</wsse:Password>"
            + "<wsse:Nonce EncodingType=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary\">" + requestHeader.security.usernameToken.nonce._ + "</wsse:Nonce>"
            + "<wsse:Created xmlns=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\">" + requestHeader.security.usernameToken.created._ + "</wsse:Created>"
            + '</wsse:UsernameToken>'
            + '</wsse:Security>'
        
        header += '</SOAP-ENV:Header>'

    header += '<SOAP-ENV:Body>'

    return header

def envelopeFooter():
    return '</SOAP-ENV:Body>' + '</SOAP-ENV:Envelope>'

def passwordDigest(self):
    timestamp = (datetime.datetime.fromtimestamp((self.timeShift or 0) + time.time())).isoformat()
    nonce = bytearray(16)
    nonce.write(struct.pack('<L', random.randint(0, 0xFFFFFFFF)), 0)
    nonce.write(struct.pack('<L', random.randint(0, 0xFFFFFFFF)), 4)
    nonce.write(struct.pack('<L', random.randint(0, 0xFFFFFFFF)), 8)
    nonce.write(struct.pack('<L', random.randint(0, 0xFFFFFFFF)), 12)
    passDigest = base64.b64encode(hashlib.sha1(nonce + timestamp.encode('ascii') + self.password.encode('ascii')).digest())
    return {
        'passDigest': passDigest,
        'nonce': base64.b64encode(nonce),
        'timestamp': timestamp,
    }
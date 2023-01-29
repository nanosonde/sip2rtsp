
import re
import json
import logging
import time
import struct
import base64
import random
import hashlib
import datetime
import xml.etree.ElementTree as ET

from typing import Tuple, Dict
from collections import defaultdict

logger = logging.getLogger(__name__)

decapitalize = lambda s: s[:1].lower() + s[1:] if s else ''

def getMethodNameFromBody(body: Dict[str, any]) -> str:
    if len(body) != 2:
        raise ValueError(f"Invalid SOAP body: expected only a namespace and method name: {body}")
    if list(body.keys())[0] != "$NS":
        raise ValueError(f"Invalid SOAP body: first entry is not a namespace: {body}")
    return list(body.keys())[1]

def getServiceNameFromOnvifNS(ns: str) -> str:
    match = re.search(r"http://www.onvif.org/(\S*)/(\S*)/wsdl", ns)
    if match:
        if match.group(1) == "ver10" or match.group(1) == "ver20":
            return match.group(2)
        else: 
            raise ValueError(f"Invalid ONVIF version in namespace: {ns} - expected ver10 or ver20")
    else:
        return None

def getNSAndTag(s: str) -> Tuple[str, str]:
    match = re.search(r"\{(.*)\}(.*)", s)
    if match:
        if match.group(1) == "":
            return None, match.group(2)
        else:
            return match.group(1), match.group(2)
    else:
        return None, s

def etree_to_dict(t: ET.Element) -> Dict[str, any]:
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

def parseSOAPString(rawXml: str) -> Dict[str, any]:
    
    root = ET.fromstring(rawXml)

    # There might be no SOAP header
    headerDict = None

    # Envelope element is already the root element
    header_element = root.find('./{http://www.w3.org/2003/05/soap-envelope}Header')
    if  header_element is not None:
        if len(header_element) > 1:
            raise ValueError('Invalid ONVIF SOAP envelope: more than one header element found')

        # For debugging
        # for elem in header_element[0].iter():
        #     tag = elem.tag
        #     [ns, tagname] = getNSAndTag(tag)
        #     logger.info(f"elem: ns: {ns} tag: {tagname} - attrib: {elem.attrib}")
        if len(header_element) > 0:
            headerDict = etree_to_dict(header_element[0])

    # Envelope element is already the root element
    body_element = root.find('./{http://www.w3.org/2003/05/soap-envelope}Body')
    if  body_element is None:
        raise ValueError('Invalid ONVIF SOAP envelope: no Body element found')

    if len(body_element) > 1:
        raise ValueError('Invalid ONVIF SOAP envelope: more than one body element found')

    # Use the single body element
    if body_element[0] is None:
        raise ValueError('Invalid ONVIF SOAP envelope: no valid element found in Body')

    # For debugging
    # for elem in body_element[0].iter():
    #     tag = elem.tag
    #     [ns, tagname] = getNSAndTag(tag)
    #     logger.info(f"elem: ns: {ns} tag: {tagname} - attrib: {elem.attrib}")

    bodyDict = etree_to_dict(body_element[0])

    soapDict = {'header': headerDict, 'body': bodyDict}
    return soapDict

def envelopeHeader(requestHeader: dict) -> str:
    header = '''<?xml version="1.0" encoding="UTF-8"?>
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

        if "MessageID" in requestHeader:
            header += '<wsa5:MessageID>' + requestHeader.messageID + '</wsa5:MessageID>'

        if "ReplyTo" in requestHeader:
            header += '<wsa5:ReplyTo SOAP-ENV:mustUnderstand="1">' + '<wsa5:Address>' + requestHeader["replyTo"]["address"] + '</wsa5:Address>' + '</wsa5:ReplyTo>'
    
        if "To" in requestHeader:
            header += "<wsa5:To SOAP-ENV:mustUnderstand=\"1\">" + requestHeader.to._ + "</wsa5:To>"

        if "Action" in requestHeader:
            header += "<wsa5:Action SOAP-ENV:mustUnderstand=\"1\">" + requestHeader.action._.replace("Request$", "Response") + "</wsa5:Action>"
        
        if "Security" in requestHeader:  
            username = requestHeader["Security"]["UsernameToken"]["Username"]
            password = requestHeader["Security"]["UsernameToken"]["Password"]["#text"]
            nonce = requestHeader["Security"]["UsernameToken"]["Nonce"]["#text"]
            created = requestHeader["Security"]["UsernameToken"]["Created"]
            header += '''
            <wsse:Security>
               <wsse:UsernameToken>
                <wsse:Username>{username}</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{password}</wsse:Password>
                <wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce}</wsse:Nonce>
                <wsse:Created xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">{created}</wsse:Created>
               </wsse:UsernameToken>
            </wsse:Security>
            '''.format(username=username, password=password, nonce=nonce, created=created)
        header += '</SOAP-ENV:Header>'

    header += '<SOAP-ENV:Body>'

    return header

def envelopeFooter() -> str:
    return '</SOAP-ENV:Body>' + '</SOAP-ENV:Envelope>'

def passwordDigest(self) -> dict:
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

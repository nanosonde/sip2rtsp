"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.OnvifServer = void 0;
const bind_decorator_1 = __importDefault(require("bind-decorator"));
const xml2js_1 = __importDefault(require("xml2js"));
const process_1 = __importDefault(require("process"));
const http_1 = __importDefault(require("http"));
const crypto_1 = __importDefault(require("crypto"));
//import util from 'util';
const buffer_1 = require("buffer");
const serviceDevice_1 = require("./serviceDevice");
const serviceMedia_1 = require("./serviceMedia");
const servicePtz_1 = require("./servicePtz");
const serviceImaging_1 = require("./serviceImaging");
const serviceEvents_1 = require("./serviceEvents");
const conf = {
    port: parseInt(process_1.default.env.PORT || "10101"),
    hostname: process_1.default.env.HOSTNAME || 'localhost',
};
const verbose = process_1.default.env.VERBOSE || true;
class OnvifServer {
    constructor() {
        this.username = "admin";
        this.password = "admin";
        this.methods = new Map();
        this.server = http_1.default.createServer(this.listener);
    }
    registerMethod(serviceName, methodname, handler) {
        this.methods.set(serviceName + ":" + methodname, handler);
    }
    startServer(port) {
        this.server.listen(port, () => {
            if (verbose) {
                if (this.server) {
                    const la = this.server.address();
                    console.log(`Listening on ${la.address} - port: ${la.port}`);
                }
            }
        });
    }
    listener(req, res) {
        req.setEncoding('utf8');
        const buf = [];
        let request;
        req.on('data', (chunk) => buf.push(chunk));
        req.on('end', () => {
            //console.log("IsBuffer? " + Buffer.isBuffer(buf) ? "true" : "false");
            if (buffer_1.Buffer.isBuffer(buf)) {
                request = buffer_1.Buffer.concat(buf);
            }
            else {
                request = buf.join('');
            }
            if (verbose) {
                //console.log("HTTP Request Header: " + util.inspect(req.headers, false, null, true));
            }
            if (req.method == "POST") {
                this.handlePOSTRequest(request.toString(), res);
            }
            else {
                console.error("Unhandled HTTP method: " + req.method);
            }
        });
    }
    ;
    getAttrAndElement(input) {
        const attr = Object.keys(input)[0];
        const element = Object.keys(input)[1];
        // console.log(`getAttrAndElement() attr: ${util.inspect(input[attr], false, null, true)}`);
        // console.log(`getAttrAndElement() element: ${util.inspect(input[element], false, null, true)}`);
        // console.log(`getAttrAndElement size(): ${util.inspect( Object.keys(input as { [key: string]: any }).length, false, null, true)}`);
        return [input[attr], element, input[element]];
    }
    async handlePOSTRequest(request, res) {
        //console.log("Raw HTTP Body: " + request);
        const [data, rawxml] = await this.parseSOAPString(request);
        //console.log(`raw data: ${util.inspect(data, false, null, true)}`);
        let [_, command, commandArgs] = this.getAttrAndElement(data.envelope.body);
        let [attr] = this.getAttrAndElement(commandArgs);
        delete commandArgs['$'];
        const reNS = /http:\/\/www.onvif.org\/\S*\/(\S*)\/wsdl/;
        let ns = '';
        const tmpNS = reNS.exec(attr['xmlns']);
        if (tmpNS) {
            ns = tmpNS[1];
        }
        if (verbose) {
            console.log('received', ns, command);
        }
        res.setHeader('Content-Type', 'application/soap+xml;charset=UTF-8');
        let content;
        let handler;
        const callHandler = async (handler, commandArgs, data) => {
            let result = handler(commandArgs, data.envelope.header);
            let envelopeBody = '';
            if (result instanceof (Promise)) {
                envelopeBody = await result;
            }
            else {
                envelopeBody = result;
            }
            content = this.envelopeHeader(data.envelope.header) + envelopeBody + this.envelopeFooter();
            res.end(content);
        };
        handler = this.methods.get(ns + ":" + command);
        if (handler) {
            await callHandler(handler, commandArgs, data);
            return;
        }
        else {
            // last resort: try to find anything that looks like this method call			
            let entries = Array.from(this.methods.entries());
            for (let i = 0; i < entries.length; i++) {
                let [key, value] = entries[i];
                if (key.includes(command)) {
                    await callHandler(value, commandArgs, data);
                    return;
                }
            }
            ;
            // we did not find anything.
            console.error("No service/method combo found!");
            res.end("");
        }
    }
    /**
     * Parse SOAP response
     */
    async parseSOAPString(rawXml) {
        const rePrefixMatch = /(?!xmlns)^.*:/;
        const result = await xml2js_1.default.parseStringPromise(rawXml, {
            tagNameProcessors: [(tag) => {
                    const str = tag.replace(rePrefixMatch, '');
                    const secondLetter = str.charAt(1);
                    if (secondLetter && secondLetter.toUpperCase() !== secondLetter) {
                        return str.charAt(0).toLowerCase() + str.slice(1);
                    }
                    return str;
                }],
            mergeAttrs: false,
            ignoreAttrs: false,
            normalizeTags: false,
            explicitArray: false,
            explicitRoot: true
        });
        //console.log(`result: ${util.inspect(result, false, null, true)}`);
        if (!result || !result.envelope || !result.envelope.body) {
            throw new Error('Wrong ONVIF SOAP response');
        }
        return [result, rawXml];
    }
    passwordDigest() {
        const timestamp = (new Date((process_1.default.uptime() * 1000) + (this.timeShift || 0))).toISOString();
        const nonce = buffer_1.Buffer.allocUnsafe(16);
        nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 0, 4);
        nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 4, 4);
        nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 8, 4);
        nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 12, 4);
        const cryptoDigest = crypto_1.default.createHash('sha1');
        cryptoDigest.update(buffer_1.Buffer.concat([nonce, buffer_1.Buffer.from(timestamp, 'ascii'), buffer_1.Buffer.from(this.password, 'ascii')]));
        const passDigest = cryptoDigest.digest('base64');
        return {
            passDigest,
            nonce: nonce.toString('base64'),
            timestamp,
        };
    }
    /**
    * Envelope header for all SOAP messages
    * @param openHeader
    * @private
    */
    envelopeHeader(requestHeader) {
        let header = '<?xml version="1.0" encoding="UTF-8"?>'
            + '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:chan="http://schemas.microsoft.com/ws/2005/02/duplex" xmlns:wsa5="http://www.w3.org/2005/08/addressing" xmlns:c14n="http://www.w3.org/2001/10/xml-exc-c14n#" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:xenc="http://www.w3.org/2001/04/xmlenc#" xmlns:wsc="http://schemas.xmlsoap.org/ws/2005/02/sc" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:xmime5="http://www.w3.org/2005/05/xmlmime" xmlns:xmime="http://tempuri.org/xmime.xsd" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:tt="http://www.onvif.org/ver10/schema" xmlns:wsrfbf="http://docs.oasis-open.org/wsrf/bf-2" xmlns:wstop="http://docs.oasis-open.org/wsn/t-1" xmlns:wsrfr="http://docs.oasis-open.org/wsrf/r-2" xmlns:tds="http://www.onvif.org/ver10/device/wsdl" xmlns:tev="http://www.onvif.org/ver10/events/wsdl" xmlns:wsnt="http://docs.oasis-open.org/wsn/b-2" xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl" xmlns:trt="http://www.onvif.org/ver10/media/wsdl" xmlns:timg="http://www.onvif.org/ver20/imaging/wsdl" xmlns:tmd="http://www.onvif.org/ver10/deviceIO/wsdl" xmlns:tns1="http://www.onvif.org/ver10/topics" xmlns:ter="http://www.onvif.org/ver10/error" xmlns:tnsaxis="http://www.axis.com/2009/event/topics">';
        //console.log(`data.envelope.header: ${util.inspect(requestHeader, false, null, true)}`);
        if (requestHeader) {
            header += '<SOAP-ENV:Header>';
            if (requestHeader.messageID) {
                header += `<wsa5:MessageID>${requestHeader.messageID}</wsa5:MessageID>`;
            }
            if (requestHeader.replyTo) {
                header += '<wsa5:ReplyTo SOAP-ENV:mustUnderstand="1">'
                    + `<wsa5:Address>${requestHeader.replyTo.address}</wsa5:Address>`
                    + '</wsa5:ReplyTo>';
            }
            if (requestHeader.to) {
                header += `<wsa5:To SOAP-ENV:mustUnderstand="1">${requestHeader.to._}</wsa5:To>`;
            }
            if (requestHeader.action) {
                header += `<wsa5:Action SOAP-ENV:mustUnderstand="1">${requestHeader.action._.replace(/Request$/, "Response")}</wsa5:Action>`;
            }
            if (requestHeader.security) {
                header += '<wsse:Security>'
                    + '<wsse:UsernameToken>'
                    + `<wsse:Username>${requestHeader.security.usernameToken.username}</wsse:Username>`
                    + `<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">${requestHeader.security.usernameToken.password._}</wsse:Password>`
                    + `<wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">${requestHeader.security.usernameToken.nonce._}</wsse:Nonce>`
                    + `<wsse:Created xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">${requestHeader.security.usernameToken.created._}</wsse:Created>`
                    + '</wsse:UsernameToken>'
                    + '</wsse:Security>';
            }
            header += '</SOAP-ENV:Header>';
        }
        header += '<SOAP-ENV:Body>';
        return header;
    }
    /**
    * Envelope footer for all SOAP messages
    * @private
    */
    envelopeFooter() {
        return '</SOAP-ENV:Body>'
            + '</SOAP-ENV:Envelope>';
    }
    stopServer() {
        this.server.close();
        if (verbose) {
            console.log('Stopped OnvifServer');
        }
    }
}
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "registerMethod", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "startServer", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "listener", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "getAttrAndElement", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "handlePOSTRequest", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "parseSOAPString", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "envelopeHeader", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "envelopeFooter", null);
__decorate([
    bind_decorator_1.default
], OnvifServer.prototype, "stopServer", null);
exports.OnvifServer = OnvifServer;
let server = new OnvifServer();
let deviceService = new serviceDevice_1.DeviceService(server);
let mediaService = new serviceMedia_1.MediaService(server);
let ptzService = new servicePtz_1.PtzService(server);
let imagingService = new serviceImaging_1.ImagingService(server);
let eventsService = new serviceEvents_1.EventsService(server);
server.startServer(conf.port);
//# sourceMappingURL=serverMockup.js.map
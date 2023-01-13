import bind from 'bind-decorator';
import xml2js from 'xml2js';
import process from 'process';
import http from 'http';
import { AddressInfo } from 'net';
import crypto from 'crypto';
//import util from 'util';
import { Buffer } from 'buffer';

import { DeviceService } from "./serviceDevice";
import { MediaService } from "./serviceMedia";
import { PtzService } from "./servicePtz";
import { ImagingService } from "./serviceImaging";
import { EventsService } from "./serviceEvents";

const conf = {
	port: parseInt(process.env.PORT || "10101" ), // server port
	hostname: process.env.HOSTNAME || 'localhost',
};

const verbose: boolean = ((process.env.VERBOSE?.toLowerCase()) === "true" || (process.env.VERBOSE?.toLowerCase()) === "1") ;

export type ServiceMethodHandler = ((args: any, header?: any) => string) | ((args: any, header?: any) => Promise<string>);

export class OnvifServer {

	private server: http.Server;
	private username: string;
	private password: string;
	private timeShift?: number;
	private methods: Map<string, ServiceMethodHandler>;

	constructor() {
		this.username = "admin";
		this.password = "admin";
		this.methods = new Map();
		this.server = http.createServer(this.listener);
	}

	@bind
	public registerMethod(serviceName: string, methodname: string, handler: ServiceMethodHandler) {
		this.methods.set(serviceName + ":" + methodname, handler);
	}

	@bind
	public startServer(port: number) {
		this.server.listen(port, () => {
			if (this.server) {
				const la = this.server.address() as AddressInfo;
				console.log(`ONVIF-Server listening on ${la.address} - port: ${la.port}`);
			}
		});
	}

	@bind
	private listener(req: http.IncomingMessage, res: http.ServerResponse): void {
		req.setEncoding('utf8');

		const buf: any[] | Uint8Array[] = [];
		let request: string | Buffer;

		req.on('data', (chunk) => buf.push(chunk));
		req.on('end', () => {
			//console.log("IsBuffer? " + Buffer.isBuffer(buf) ? "true" : "false");
			if (Buffer.isBuffer(buf)) {
				request = Buffer.concat(buf);
			} else {
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
	};
	
	@bind
	private getAttrAndElement(input: Record<string,any>): any {
		
		const attr = Object.keys(input as { [key: string]: any })[0];
		const element = Object.keys(input as { [key: string]: any })[1];
		// console.log(`getAttrAndElement() attr: ${util.inspect(input[attr], false, null, true)}`);
		// console.log(`getAttrAndElement() element: ${util.inspect(input[element], false, null, true)}`);
		// console.log(`getAttrAndElement size(): ${util.inspect( Object.keys(input as { [key: string]: any }).length, false, null, true)}`);

		return [input[attr], element, input[element]];
	}

	@bind
	private async handlePOSTRequest(request: string, res: http.ServerResponse) {

		//console.log("Raw HTTP Body: " + request);
		const [data, rawxml] = await this.parseSOAPString(request);
		//console.log(`raw data: ${util.inspect(data, false, null, true)}`);

		let [_, command, commandArgs] = this.getAttrAndElement(data.envelope.body);
		let [attr] = this.getAttrAndElement(commandArgs);
		delete commandArgs['$'];

		const reNS: RegExp = /http:\/\/www.onvif.org\/\S*\/(\S*)\/wsdl/;

		let ns='';
		const tmpNS = reNS.exec(attr['xmlns']);
		if (tmpNS) {
			ns = tmpNS[1];
		}

		if (verbose) {
			console.log('received', ns, command);
		}

		res.setHeader('Content-Type', 'application/soap+xml;charset=UTF-8');

		let content: string | undefined;
		let handler: ServiceMethodHandler | undefined;

		const callHandler = async (handler: ServiceMethodHandler, commandArgs: any, data: any): Promise<void> => {
			let result = handler(commandArgs, data.envelope.header);
			let envelopeBody = '';
			if (result instanceof Promise<string>) {
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
					await callHandler(value, commandArgs, data)
					return;
				}
			};
			// we did not find anything.
			console.error("No service/method combo found!");
			res.end("");
		}
	}

	/**
	 * Parse SOAP response
	 */
	@bind
	async parseSOAPString(rawXml: string): Promise<[Record<string, any>, string]> {

		const rePrefixMatch = /(?!xmlns)^.*:/;
		
		const result = await xml2js.parseStringPromise(rawXml, {
			tagNameProcessors : [(tag) => {
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
			
	private passwordDigest() {
		const timestamp = (new Date((process.uptime() * 1000) + (this.timeShift || 0))).toISOString();
		const nonce = Buffer.allocUnsafe(16);
		nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 0, 4);
		nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 4, 4);
		nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 8, 4);
		nonce.writeUIntLE(Math.ceil(Math.random() * 0x100000000), 12, 4);
		const cryptoDigest = crypto.createHash('sha1');
		cryptoDigest.update(Buffer.concat([nonce, Buffer.from(timestamp, 'ascii'), Buffer.from(this.password!, 'ascii')]));
		const passDigest = cryptoDigest.digest('base64');
		return {
			passDigest,
			nonce : nonce.toString('base64'),
			timestamp,
		};
	}
	
   /**
   * Envelope header for all SOAP messages
   * @param openHeader
   * @private
   */
	@bind
	private envelopeHeader(requestHeader: any) {

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
	 @bind
	 private envelopeFooter() {
	 return '</SOAP-ENV:Body>'
		  + '</SOAP-ENV:Envelope>';
	 }
 

    @bind
	public stopServer() {
		this.server.close();

		if (verbose) {
			console.log('Stopped OnvifServer');
		}
	}	
}

let server = new OnvifServer();
let deviceService = new DeviceService(server);
let mediaService = new MediaService(server);
let ptzService = new PtzService(server);
let imagingService = new ImagingService(server);
let eventsService = new EventsService(server);
server.startServer(conf.port);

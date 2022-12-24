export type ServiceMethodHandler = ((args: any, header?: any) => string) | ((args: any, header?: any) => Promise<string>);
export declare class OnvifServer {
    private server;
    private username;
    private password;
    private timeShift?;
    private methods;
    constructor();
    registerMethod(serviceName: string, methodname: string, handler: ServiceMethodHandler): void;
    startServer(port: number): void;
    private listener;
    private getAttrAndElement;
    private handlePOSTRequest;
    /**
     * Parse SOAP response
     */
    parseSOAPString(rawXml: string): Promise<[Record<string, any>, string]>;
    private passwordDigest;
    /**
    * Envelope header for all SOAP messages
    * @param openHeader
    * @private
    */
    private envelopeHeader;
    /**
    * Envelope footer for all SOAP messages
    * @private
    */
    private envelopeFooter;
    stopServer(): void;
}

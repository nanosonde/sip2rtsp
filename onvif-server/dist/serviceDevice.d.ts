import { OnvifServer } from "./serverMockup";
export declare class DeviceService {
    readonly serviceName = "device";
    interfaceName: string;
    listenIp: string;
    listenPort: string;
    serviceAddress: string;
    constructor(server: OnvifServer);
    private getSystemDateAndTime;
    private getScopes;
    private getDeviceInformation;
    private getNetworkInterfaces;
    private getDNS;
    private getServices;
    private getCapabilities;
    private getZeroConfiguration;
    private getServiceCapabilities;
    private setSystemFactoryDefault;
    private systemReboot;
    private getNTP;
    private getNetworkDefaultGateway;
    private getNetworkProtocols;
    private getHostname;
    private getDiscoveryMode;
    private getUsers;
    private getCertificates;
    private getCertificatesStatus;
    private getRelayOutputs;
}

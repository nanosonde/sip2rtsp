import { OnvifServer } from "./serverMockup";
export declare class EventsService {
    readonly serviceName = "events";
    interfaceName: string;
    listenIp: string;
    listenPort: string;
    serviceAddress: string;
    private subscriptions;
    constructor(server: OnvifServer);
    private getSubscriptionIdFromToHeader;
    private createPullPointSubscription;
    private unsubscribe;
    private pullMessages;
    private renew;
    private getEventProperties;
}

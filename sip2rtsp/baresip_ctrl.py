import logging
import pynetstring
import json
import asyncio

from sip2rtsp.const import BARESIP_CTRL_PORT

logger = logging.getLogger(__name__)


class BaresipCtrlProtocol(asyncio.Protocol):
    def __init__(self, on_con_lost):
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        logger.info("Connection established")
        # transport.write(self.message.encode())
        # print("Data sent: {!r}".format(self.message))

    def data_received(self, rawdata):
        s = pynetstring.decode(rawdata.decode())
        data = json.loads(s[0])
        logger.debug("Data received: {data}".format(data=data))
        if data["event"] == True:
            logger.debug("Event received")

    def connection_lost(self, exc):
        logger.info("Connection closed.")
        if not self.on_con_lost.cancelled():
            self.on_con_lost.set_result(True)


class BareSipControl:
    def __init__(self, loop) -> None:
        self.loop = loop

    async def run_client(self):
        on_con_lost = self.loop.create_future()

        transport, protocol = await self.loop.create_connection(
            lambda: BaresipCtrlProtocol(on_con_lost), "127.0.0.1", 4444
        )

        # Wait until the protocol signals that the connection
        # is lost and close the transport.
        try:
            await on_con_lost
        except asyncio.CancelledError:
            logger.debug(f'run_client(): future "on_con_lost" cancelled')
        finally:
            logger.debug(f"Closing transport...")
            transport.close()

import logging
import asyncio
import json
import uuid
import pynetstring

logger = logging.getLogger(__name__)


class BaresipProtocol(asyncio.Protocol):
    def __init__(self, baresip_control):
        self.baresip_control = baresip_control

    def connection_made(self, _):
        logger.info("Baresip control connection established")

    def data_received(self, data):
        # logger.debug("Data received: {data}".format(data=data))
        self.baresip_control.handle_data(data)

    def connection_lost(self, exc):
        logger.info("Baresip control connection lost")
        self.baresip_control.handle_connection_lost(exc)


class BaresipControl:
    def __init__(self, host, port, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.transport = None
        self.pending_requests = {}
        self.callback = None

    async def start(self):
        self.transport, _ = await asyncio.get_running_loop().create_connection(
            lambda: BaresipProtocol(self), self.host, self.port
        )

    def stop(self):
        self.transport.close()

    def set_callback(self, callback):
        """Set the callback function to be called when an event is signalled"""
        self.callback = callback

    async def callstat(self):
        """Get current call details"""
        token = str(uuid.uuid4())
        command = {"command": "callstat", "params": "", "token": token}
        future = asyncio.Future()
        self.pending_requests[token] = future
        self._send_command(command)
        return await asyncio.wait_for(future, timeout=self.timeout)

    async def listcalls(self):
        """List active calls"""
        token = str(uuid.uuid4())
        command = {"command": "listcalls", "params": "", "token": token}
        future = asyncio.Future()
        self.pending_requests[token] = future
        self._send_command(command)
        return await asyncio.wait_for(future, timeout=self.timeout)

    async def dial(self, sip_address):
        """Initiate a call to the specified SIP address"""
        token = str(uuid.uuid4())
        command = {"command": "dial", "params": sip_address, "token": token}
        future = asyncio.Future()
        self.pending_requests[token] = future
        self._send_command(command)
        return await asyncio.wait_for(future, timeout=self.timeout)

    async def hangup(self):
        """Hang up the current call"""
        token = str(uuid.uuid4())
        command = {"command": "hangup", "token": token}
        future = asyncio.Future()
        self.pending_requests[token] = future
        self._send_command(command)
        return await asyncio.wait_for(future, timeout=self.timeout)

    async def accept(self):
        """Accept the incoming call"""
        token = str(uuid.uuid4())
        command = {"command": "accept", "token": token}
        future = asyncio.Future()
        self.pending_requests[token] = future
        self._send_command(command)
        return await asyncio.wait_for(future, timeout=self.timeout)

    def _send_command(self, command):
        """Send a command to the Baresip instance"""
        netstring = pynetstring.encode(json.dumps(command).encode())
        # logger.debug("Data sent: {netstring}".format(netstring=netstring))
        self.transport.write(netstring)

    def _receive(self, data):
        """Receive and process data from the Baresip instance"""
        if "response" in data:
            token = data["token"]
            future = self.pending_requests.pop(token, None)
            if future:
                if data["ok"]:
                    future.set_result(data["data"])
                else:
                    future.set_exception(Exception(data["data"]))
        elif "event" in data:
            if self.callback:
                self.callback(data)

    def handle_data(self, data):
        s = pynetstring.decode(data.decode())
        for se in s:
            response = json.loads(se)
            self._receive(response)

    def handle_connection_lost(self, exc):
        pass

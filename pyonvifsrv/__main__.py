import asyncio
import logging

from pyonvifsrv.server import OnvifServer

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s] %(name)-25s %(levelname)-8s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )

    loop = asyncio.get_event_loop()

    onvifServer = OnvifServer(loop, None)

    loop.create_task(onvifServer.start_server())
    loop.run_forever()


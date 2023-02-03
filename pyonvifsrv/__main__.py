import asyncio
import logging

from pyonvifsrv.server import OnvifServer

logger = logging.getLogger(__name__)

class CustomFormatter(logging.Formatter):

    white = "\x1b[97;20m"
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    fmt = "%(asctime)s - {}%(levelname)-8s{} - %(name)-25s - %(message)s" #.%(funcName)s
    #fmt = "%(asctime)s - %(name)-25s {}%(levelname)-8s{}: %(message)s"

    FORMATS = {
        logging.DEBUG: fmt.format(grey, reset),
        logging.INFO: fmt.format(green, reset),
        logging.WARNING: fmt.format(yellow, reset),
        logging.ERROR: fmt.format(red, reset),
        logging.CRITICAL: fmt.format(bold_red, reset),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

if __name__ == "__main__":
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[handler]
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    onvifServer = OnvifServer(loop, None)

    loop.create_task(onvifServer.start_server())
    loop.run_forever()


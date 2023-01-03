import logging
import multiprocessing as mp
from multiprocessing.queues import Queue
import time

from sip2rtsp.version import VERSION
from sip2rtsp.log import log_process, root_configurer

logger = logging.getLogger(__name__)

class Sip2RtspApp:
    def __init__(self) -> None:
        self.log_queue: Queue = mp.Queue()

    def init_logger(self) -> None:
            self.log_process = mp.Process(
                target=log_process, args=(self.log_queue,), name="log_process"
            )
            self.log_process.daemon = True
            self.log_process.start()
            root_configurer(self.log_queue)

    def start(self) -> None:
            self.init_logger()
            logger.info(f"Starting SIP2RTSP ({VERSION})")

            while True:
                time.sleep(1)

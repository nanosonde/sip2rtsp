import faulthandler

faulthandler.enable()
from sip2rtsp.gi import GLib  # noqa: F401

import threading
import signal
from typing import Optional
from types import FrameType
import logging
import time

threading.current_thread().name = "sip2rtsp"

from sip2rtsp.app import Sip2RtspApp

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    loop = GLib.MainLoop()

    thread = threading.Thread(target=loop.run)

    sip2rtsp_app = Sip2RtspApp(loop)

    def receiveSignal(signalNumber: int, frame: Optional[FrameType]) -> None:
        logger.info(f"Received SIGINT...")
        sip2rtsp_app.stop()
        logger.info(f"Quitting glib main loop...")
        loop.quit()
        logger.info(f"Done.")
        logger.info(f"Waiting for glib thread to join...")
        thread.join()
        logger.info(f"Done.")

    signal.signal(signal.SIGINT, receiveSignal)

    sip2rtsp_app.start()

    thread.start()

import faulthandler

faulthandler.enable()
import threading

threading.current_thread().name = "sip2rtsp"

from sip2rtsp.gi import Gst  # noqa: F401

from sip2rtsp.app import Sip2RtspApp

if __name__ == "__main__":
    sip2rtsp_app = Sip2RtspApp()

    sip2rtsp_app.start()

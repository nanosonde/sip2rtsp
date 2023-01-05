import logging
import multiprocessing as mp
from multiprocessing.queues import Queue

from sip2rtsp.version import VERSION
from sip2rtsp.log import log_process, root_configurer

from .gi import GLib, Gst, GstRtspServer

logger = logging.getLogger(__name__)

#launch_string = f"videotestsrc is-live=true ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 audiotestsrc is-live=true ! mulawenc ! rtppcmupay name=pay1"             
#launch_string = f"rtspsrc location=rtsp://10.10.10.10:8554/gartentor_h264_ext name=rtspsrc ! decodebin ! videoconvert ! videoscale ! videorate ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 rtspsrc. ! decodebin ! audioconvert ! audioresample ! audio/x-raw ! opusenc ! rtpopuspay name=pay1"         pulsesrc device=\"BaresipSpeakerInput\"                 
#gst-launch-1.0 -v audiotestsrc ! audioconvert ! pulsesink device="BaresipMicrophone" pulsesrc device="BaresipSpeaker.monitor" ! audioconvert ! audioresample ! wavenc ! filesink location=test.wa
launch_string = f"souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=true timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=50 key-int-max=70 ! h264parse ! rtph264pay config-interval=1 name=pay0 pt=96 pulsesrc device=\"BaresipSpeakerInput\" do-timestamp=true ! queue ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! opusenc ! rtpopuspay name=pay1"
#launch_string = f"souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=false timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=60 key-int-max=60 ! rtph264pay config-interval=-1 name=pay0 pt=96 pulsesrc device=\"BaresipSpeaker.monitor\" ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 !  mulawenc ! rtppcmupay name=pay1"

def media_prepared(media):
    print("media_prepared(): media: {media}, status: {status}".format(media=str(media), status=media.get_status()), flush=True)

    n_streams = media.n_streams()
    print("media_configure(): number of streams: {num}".format(num=n_streams), flush=True)
    for n in range(n_streams):
        print("stream {n}: media_configure(): ssrc: {ssrc}".format(n=n,ssrc=media.get_stream(n).get_ssrc()), flush=True)
        Gst.debug_bin_to_dot_file(media.get_stream(n).get_joined_bin(), Gst.DebugGraphDetails.ALL, "stream" + str(n))
        #media.get_stream(n).set_blocked(False)

def media_configure(factory, media):
    print("media_configure(): media: {media}, status: {status}".format(media=str(media), status=media.get_status()), flush=True)
    media.connect("prepared", media_prepared)
    Gst.debug_bin_to_dot_file(media.get_element(), Gst.DebugGraphDetails.ALL, "media-configure")
    n_streams = media.n_streams()
    print("media_configure(): number of streams: {num}".format(num=n_streams), flush=True)


class Sip2RtspApp:
    def __init__(self) -> None:
        self.log_queue: Queue = mp.Queue()
        self.loop = GLib.MainLoop()
        self.server = GstRtspServer.RTSPOnvifServer.new()
        self.factory = GstRtspServer.RTSPOnvifMediaFactory.new()
        self.factory.set_media_gtype(GstRtspServer.RTSPOnvifMedia)
        self.factory.set_launch(launch_string)
        #self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! fakesink async=false )")
        #self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec ! wavenc ! filesink location=test.wav async=false )")
        self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! pulsesink device=\"BaresipMicrophone\" async=false )")
        #self.factory.set_backchannel_bandwidth(2000)
        self.factory.set_shared(False)
        self.factory.set_latency(200)
        self.factory.set_enable_rtcp(False)
        #self.factory.set_protocols(GstRtsp.RTSPLowerTrans.TCP)
        #self.factory.set_profiles(GstRtsp.RTSPProfile.AVP)
        self.factory.connect("media-configure", media_configure)
        self.server.get_mount_points().add_factory("/test", self.factory)

        self.server.attach()


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

            self.loop.run()

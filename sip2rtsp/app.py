import logging

from sip2rtsp.version import VERSION

from .gi import GstRtspServer

logger = logging.getLogger(__name__)

# launch_string = f"videotestsrc is-live=true ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 audiotestsrc is-live=true ! mulawenc ! rtppcmupay name=pay1"
# launch_string = f"rtspsrc location=rtsp://10.10.10.10:8554/gartentor_h264_ext name=rtspsrc ! decodebin ! videoconvert ! videoscale ! videorate ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 rtspsrc. ! decodebin ! audioconvert ! audioresample ! audio/x-raw ! opusenc ! rtpopuspay name=pay1"         pulsesrc device=\"BaresipSpeakerInput\"
# gst-launch-1.0 -v audiotestsrc ! audioconvert ! pulsesink device="BaresipMicrophone" pulsesrc device="BaresipSpeaker.monitor" ! audioconvert ! audioresample ! wavenc ! filesink location=test.wa
launch_string = f'souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=true timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=50 key-int-max=70 ! h264parse ! rtph264pay config-interval=1 name=pay0 pt=96 pulsesrc device="BaresipSpeakerInput" do-timestamp=true ! queue ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! opusenc ! rtpopuspay name=pay1'
# launch_string = f"souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=false timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=60 key-int-max=60 ! rtph264pay config-interval=-1 name=pay0 pt=96 pulsesrc device=\"BaresipSpeaker.monitor\" ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 !  mulawenc ! rtppcmupay name=pay1"


class Sip2RtspApp:
    def __init__(self, loop) -> None:
        self.loop = loop
        self.server = GstRtspServer.RTSPOnvifServer.new()
        self.factory = GstRtspServer.RTSPOnvifMediaFactory.new()
        self.factory.set_media_gtype(GstRtspServer.RTSPOnvifMedia)
        # self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! fakesink async=false )")
        # self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec ! wavenc ! filesink location=test.wav async=false )")
        self.factory.set_backchannel_launch(
            '( capsfilter caps="application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU" name=depay_backchannel ! rtppcmudepay ! mulawdec ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! pulsesink device="BaresipMicrophone" async=false )'
        )
        # self.factory.set_backchannel_bandwidth(2000)
        self.factory.set_shared(False)
        self.factory.set_latency(200)
        self.factory.set_enable_rtcp(False)
        # self.factory.set_protocols(GstRtsp.RTSPLowerTrans.TCP)
        # self.factory.set_profiles(GstRtsp.RTSPProfile.AVP)
        self.factory.connect("media-constructed", self.media_constructed)
        self.factory.connect("media-configure", self.media_configure)
        self.server.get_mount_points().add_factory("/test", self.factory)

        self.server.attach(self.loop.get_context())

    def start(self) -> None:
        logger.info(f"Starting SIP2RTSP ({VERSION})")
        self.factory.set_launch(launch_string)

    def stop(self) -> None:
        logger.info(f"Stopping...")

    def media_unprepared(self, media):
        logger.info(
            "media_unprepared(): media: {media}, status: {status}".format(
                media=str(media), status=media.get_status()
            )
        )

        n_streams = media.n_streams()
        logger.info(
            "media_unprepared(): number of streams: {num}".format(num=n_streams)
        )
        for n in range(n_streams):
            stream = media.get_stream(n)
            if stream:
                logger.info(
                    "media_unprepared(): stream {n}: index: {index}".format(
                        n=n, index=stream.get_index()
                    )
                )
            # Gst.debug_bin_to_dot_file(
            #     media.get_stream(n).get_joined_bin(),
            #     Gst.DebugGraphDetails.ALL,
            #     "stream" + str(n),
            # )
            # media.get_stream(n).set_blocked(False)

    def media_prepared(self, media):
        logger.info(
            "media_prepared(): media: {media}, status: {status}".format(
                media=str(media), status=media.get_status()
            )
        )

        n_streams = media.n_streams()
        logger.info("media_prepared(): number of streams: {num}".format(num=n_streams))
        for n in range(n_streams):
            stream = media.get_stream(n)
            if stream:
                logger.info(
                    "media_prepared(): stream {n}: ssrc: {ssrc}".format(
                        n=n, ssrc=stream.get_ssrc()
                    )
                )
            # Gst.debug_bin_to_dot_file(
            #     media.get_stream(n).get_joined_bin(),
            #     Gst.DebugGraphDetails.ALL,
            #     "stream" + str(n),
            # )
            # media.get_stream(n).set_blocked(False)

    def media_constructed(self, factory, media):
        logger.info(
            "media_constructed(): media: {media}, status: {status}".format(
                media=str(media), status=media.get_status()
            )
        )

        media.connect("unprepared", self.media_unprepared)
        media.connect("prepared", self.media_prepared)

        n_streams = media.n_streams()
        logger.info(
            "media_constructed(): number of streams: {num}".format(num=n_streams)
        )

    def media_configure(self, factory, media):
        logger.info(
            "media_configure(): media: {media}, status: {status}".format(
                media=str(media), status=media.get_status()
            )
        )

        # Gst.debug_bin_to_dot_file(
        #     media.get_element(), Gst.DebugGraphDetails.ALL, "media-configure"
        # )
        n_streams = media.n_streams()
        logger.info("media_configure(): number of streams: {num}".format(num=n_streams))

import asyncio
import logging

from sip2rtsp.version import VERSION
from sip2rtsp.gi import GstRtspServer, GstRtsp
from sip2rtsp.baresip_ctrl import BareSipControl

logger = logging.getLogger(__name__)

# launch_string = f"videotestsrc is-live=true ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 audiotestsrc is-live=true ! mulawenc ! rtppcmupay name=pay1"
# launch_string = f"rtspsrc location=rtsp://10.10.10.10:8554/gartentor_h264_ext name=rtspsrc ! decodebin ! videoconvert ! videoscale ! videorate ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 rtspsrc. ! decodebin ! audioconvert ! audioresample ! audio/x-raw ! opusenc ! rtpopuspay name=pay1"         pulsesrc device=\"BaresipSpeakerInput\"
# gst-launch-1.0 -v audiotestsrc ! audioconvert ! pulsesink device="BaresipMicrophone" pulsesrc device="BaresipSpeaker.monitor" ! audioconvert ! audioresample ! wavenc ! filesink location=test.wa
launch_string = f'souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=true timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=50 key-int-max=70 ! h264parse ! rtph264pay config-interval=1 name=pay0 pt=96 pulsesrc device="BaresipSpeakerInput" do-timestamp=true ! queue ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! opusenc ! rtpopuspay name=pay1'
# launch_string = f"souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=false timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=60 key-int-max=60 ! rtph264pay config-interval=-1 name=pay0 pt=96 pulsesrc device=\"BaresipSpeaker.monitor\" ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 !  mulawenc ! rtppcmupay name=pay1"


class Sip2RtspApp:
    def __init__(self, aioloop, loop) -> None:
        self.aioloop = aioloop
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
        # self.factory.connect("media-constructed", self.media_constructed)
        # self.factory.connect("media-configure", self.media_configure)
        self.server.connect("client-connected", self.client_connected)
        self.server.get_mount_points().add_factory("/test", self.factory)

        self.server.attach(self.loop.get_context())

        self.bs_ctrl = BareSipControl(self.aioloop)

        # self.stop_future = self.aioloop.create_future()

    async def start(self) -> None:
        logger.info(f"Starting SIP2RTSP ({VERSION})")
        self.factory.set_launch(launch_string)
        # try:
        await self.bs_ctrl.run_client()
        # except asyncio.CancelledError:
        #     pass
        # finally:
        #     pass

    def stop(self) -> None:
        logger.info(f"Stopping...")
        # self.stop_future.set_result(True)

    def client_play_request(self, client, context: GstRtspServer.RTSPContext):
        logger.info(
            "client_play_request(): remote ip: {remoteip}".format(
                remoteip=client.get_connection().get_ip()
            )
        )
        reqmsg: GstRtsp.RTSPMessage = context.request
        reqmsg.dump()
        res, value = reqmsg.get_header(GstRtsp.RTSPHeaderField.REQUIRE, 0)
        if res == GstRtsp.RTSPResult.OK:
            logger.info("client_play_request(): require: {value}".format(value=value))

    def client_setup_request(self, client, context: GstRtspServer.RTSPContext):
        control = context.stream.get_control()
        caps = context.stream.get_caps()
        caps = caps.to_string() if caps else "n/a"
        logger.info(
            "client_setup_request(): remote ip: {remoteip} control: {control}, caps: {caps}".format(
                remoteip=client.get_connection().get_ip(), control=control, caps=caps
            )
        )
        reqmsg: GstRtsp.RTSPMessage = context.request
        # reqmsg.dump()
        res, value = reqmsg.get_header(GstRtsp.RTSPHeaderField.REQUIRE, 0)
        if res == GstRtsp.RTSPResult.OK:
            logger.info("client_setup_request(): require: {value}".format(value=value))

    def client_describe_request(self, client, context: GstRtspServer.RTSPContext):
        logger.info(
            "client_describe_request(): remote ip: {remoteip}".format(
                remoteip=client.get_connection().get_ip()
            )
        )
        reqmsg: GstRtsp.RTSPMessage = context.request
        res, value = reqmsg.get_header(GstRtsp.RTSPHeaderField.REQUIRE, 0)
        if res == GstRtsp.RTSPResult.OK:
            logger.info(
                "client_describe_request(): require: {value}".format(value=value)
            )

    def client_send_message(self, client, _whatsthis, message):
        logger.info(
            "client_send_message(): remote ip: {remoteip} body: \n{body}".format(
                remoteip=client.get_connection().get_ip(),
                body=message.get_body().data.decode("utf-8"),
            )
        )

    def client_closed(self, client):
        logger.info(
            "client_closed(): remote ip: {remoteip}".format(
                remoteip=client.get_connection().get_ip()
            )
        )

    def client_connected(self, server, client):
        logger.info(
            "client_connected(): remote ip: {remoteip}".format(
                remoteip=client.get_connection().get_ip()
            )
        )
        client.connect("closed", self.client_closed)
        client.connect("describe-request", self.client_describe_request)
        client.connect("setup-request", self.client_setup_request)
        client.connect("play-request", self.client_play_request)
        # client.connect("send_message", self.client_send_message)

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

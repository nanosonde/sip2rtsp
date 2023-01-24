import asyncio
import logging
import os
import signal

from sip2rtsp.version import VERSION
from sip2rtsp.gi import GstRtspServer, GstRtsp
from sip2rtsp.baresip_ctrl import BaresipControl
from sip2rtsp.const import (
    BARESIP_CTRL_HOST,
    BARESIP_CTRL_PORT,
    BARESIP_CTRL_REQUEST_TIMEOUT,
    EVENT_TYPE,
)

logger = logging.getLogger(__name__)

# launch_string = f"videotestsrc is-live=true ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 audiotestsrc is-live=true ! mulawenc ! rtppcmupay name=pay1"
# launch_string = f"rtspsrc location=rtsp://10.10.10.10:8554/gartentor_h264_ext name=rtspsrc ! decodebin ! videoconvert ! videoscale ! videorate ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 rtspsrc. ! decodebin ! audioconvert ! audioresample ! audio/x-raw ! opusenc ! rtpopuspay name=pay1"         pulsesrc device=\"BaresipSpeakerInput\"
# gst-launch-1.0 -v audiotestsrc ! audioconvert ! pulsesink device="BaresipMicrophone" pulsesrc device="BaresipSpeaker.monitor" ! audioconvert ! audioresample ! wavenc ! filesink location=test.wa
launch_string = f'souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=true timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=50 key-int-max=70 ! h264parse ! rtph264pay config-interval=1 name=pay0 pt=96 pulsesrc device="BaresipSpeakerInput" do-timestamp=true ! queue ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! opusenc ! rtpopuspay name=pay1'
# launch_string = f"souphttpsrc location=http://10.10.10.10:54321/stream is-live=true do-timestamp=false timeout=5 ! multipartdemux ! jpegdec ! videoconvert ! videoscale ! videorate ! clockoverlay ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=superfast bitrate=2000 option-string=keyint=60:min-keyint=60 key-int-max=60 ! rtph264pay config-interval=-1 name=pay0 pt=96 pulsesrc device=\"BaresipSpeaker.monitor\" ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 !  mulawenc ! rtppcmupay name=pay1"


class Sip2RtspApp:
    def __init__(self, aioloop, loop, config) -> None:
        self.aioloop = aioloop
        self.loop = loop
        self.config = config

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

        # Connect gstreamer signals
        self.server.connect("client-connected", self.client_connected)
        self.server.get_mount_points().add_factory("/test", self.factory)

        # Attach gstreamer RTSP server to our GLib event loop
        self.server.attach(self.loop.get_context())

        self.bs_ctrl = BaresipControl(
            BARESIP_CTRL_HOST, BARESIP_CTRL_PORT, BARESIP_CTRL_REQUEST_TIMEOUT
        )
        self.bs_ctrl.set_callback(self.event_handler)

    def set_environment_vars(self) -> None:
        for key, value in self.config.environment_vars.items():
            os.environ[key] = value

    def set_log_levels(self) -> None:
        logging.getLogger().setLevel(self.config.logger.default.value.upper())
        for log, level in self.config.logger.logs.items():
            logging.getLogger(log).setLevel(level.value.upper())

    async def start(self) -> None:
        logger.info(f"Starting SIP2RTSP ({VERSION})")
        try:
            self.set_environment_vars()
            self.set_log_levels()
        except Exception as e:
            print(e)
            os.kill(os.getpid(), signal.SIGTERM)

        self.factory.set_launch(launch_string)

        await self.bs_ctrl.start()

    async def stop(self) -> None:
        logger.info(f"Hanging up...")
        await self.bs_ctrl.hangup()
        logger.info(f"Stopped SIP2RTSP ({VERSION})")

    def event_handler(self, data):
        # logger.debug("Event: " + str(data))
        if data["type"] == EVENT_TYPE.CALL_INCOMING:
            logger.info("Incoming call from {peeruri}".format(peeruri=data["peeruri"]))
        elif data["type"] == EVENT_TYPE.CALL_CLOSED:
            logger.info("Call closed from {peeruri}".format(peeruri=data["peeruri"]))
        elif data["type"] == EVENT_TYPE.CALL_ESTABLISHED:
            logger.info(
                "Call established from {peeruri}".format(peeruri=data["peeruri"])
            )

    def client_play_request(self, client, context: GstRtspServer.RTSPContext):
        logger.debug(
            "Received PLAY request from {remoteip}".format(
                remoteip=client.get_connection().get_ip()
            )
        )
        reqmsg: GstRtsp.RTSPMessage = context.request
        # reqmsg.dump()
        res, value = reqmsg.get_header(GstRtsp.RTSPHeaderField.REQUIRE, 0)
        if res == GstRtsp.RTSPResult.OK:
            logger.debug("PLAY request header: Require: {value}".format(value=value))

    def client_setup_request(self, client, context: GstRtspServer.RTSPContext):
        control = context.stream.get_control()
        caps = context.stream.get_caps()
        caps = caps.to_string() if caps else "n/a"
        logger.info(
            "Received SETUP request from {remoteip}: control: {control}, caps: {caps}".format(
                remoteip=client.get_connection().get_ip(), control=control, caps=caps
            )
        )
        reqmsg: GstRtsp.RTSPMessage = context.request
        # reqmsg.dump()
        res, value = reqmsg.get_header(GstRtsp.RTSPHeaderField.REQUIRE, 0)
        if res == GstRtsp.RTSPResult.OK:
            logger.debug("SETUP request header: Require: {value}".format(value=value))
            if value == "www.onvif.org/ver20/backchannel":

                async def dial():
                    logger.info("ONVIF backchannel requested. Dialing...")
                    await self.bs_ctrl.dial("sip:11@10.10.10.80")
                    logger.info("Dialing done...")

                asyncio.run_coroutine_threadsafe(dial(), self.aioloop)

    def client_describe_request(self, client, context: GstRtspServer.RTSPContext):
        logger.debug(
            "Received DESCRIBE request from: {remoteip}".format(
                remoteip=client.get_connection().get_ip()
            )
        )
        reqmsg: GstRtsp.RTSPMessage = context.request
        # reqmsg.dump()
        res, value = reqmsg.get_header(GstRtsp.RTSPHeaderField.REQUIRE, 0)
        if res == GstRtsp.RTSPResult.OK:
            logger.debug(
                "DESCRIBE request header: Require: {value}".format(value=value)
            )

    def client_closed(self, client):
        logger.debug(
            "RTSP client connection from {remoteip} closed".format(
                remoteip=client.get_connection().get_ip()
            )
        )

        async def hangup():
            logger.info("ONVIF backchannel connection was closed. Hanging up...")
            await self.bs_ctrl.hangup()
            logger.info("Hanging up done...")

        asyncio.run_coroutine_threadsafe(hangup(), self.aioloop)

    # def client_send_message(self, client, _whatsthis, message):
    #     logger.debug(
    #         "Sending message to {remoteip} body: \n{body}".format(
    #             remoteip=client.get_connection().get_ip(),
    #             body=message.get_body().data.decode("utf-8"),
    #         )
    #     )

    def client_connected(self, server, client):
        logger.info(
            "RTSP client connected from {remoteip}".format(
                remoteip=client.get_connection().get_ip()
            )
        )
        client.connect("play-request", self.client_play_request)
        client.connect("setup-request", self.client_setup_request)
        client.connect("describe-request", self.client_describe_request)
        client.connect("closed", self.client_closed)
        # client.connect("send_message", self.client_send_message)

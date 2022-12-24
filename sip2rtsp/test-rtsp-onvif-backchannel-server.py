#!/usr/bin/env python3

import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtsp', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtsp, GstRtspServer, GLib


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

class MyFactory(GstRtspServer.RTSPOnvifMediaFactory):
    def __init__(self, **properties):
        super(MyFactory, self).__init__(**properties)

        #self.launch_string = f"videotestsrc is-live=true ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 audiotestsrc is-live=true ! opusenc ! rtpopuspay name=pay1"
        #self.launch_string = f"videotestsrc is-live=true ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 audiotestsrc is-live=true ! mulawenc ! rtppcmupay name=pay1"
        #self.launch_string = f"rtspsrc location=rtsp://10.10.10.10:8554/gartentor_h264_ext name=rtspsrc ! decodebin ! videoconvert ! videoscale ! videorate ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency key-int-max=60 ! rtph264pay config-interval=1 name=pay0 pt=96 rtspsrc. ! decodebin ! audioconvert ! audioresample ! audio/x-raw ! opusenc ! rtpopuspay name=pay1"

    #def do_create_element(self, url):
    #    bin = Gst.parse_launch(self.launch_string)
    #    Gst.debug_bin_to_dot_file(bin, Gst.DebugGraphDetails.ALL, "serverbin")
    #    self.set_backchannel_launch("( capsfilter caps=\"application/x-rtp, media=audio, payload=0, clock-rate=8000, encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! fakesink async=false )")
    #    return bin

    #def do_configure(self, rtsp_media):
    #    print("do_configure")

class GstServer(GstRtspServer.RTSPOnvifServer):
    def __init__(self, **properties):
        super().__init__(**properties)
        #self.factory = MyFactory()
        self.factory = GstRtspServer.RTSPOnvifMediaFactory.new()
        #self.factory.set_media_gtype(GstRtspServer.RTSPOnvifMedia)
        self.factory.set_shared(False)
        self.factory.set_launch(launch_string)
        #self.factory.set_backchannel_launch("( rtppcmudepay name=depay_backchannel ! fakesink async=false )")
        #self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp, media=audio, payload=0, clock-rate=8000, encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec  ! fakesink async=false )")
        #self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp, media=audio, payload=0, clock-rate=8000, encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec  ! wavenc ! filesink location=test.wav async=false )")
        self.factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp, media=audio, payload=0, clock-rate=8000, encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec ! audioconvert ! audioresample ! pulsesink device=\"BaresipMicrophone\" async=false )")
        self.get_mount_points().add_factory("/test", self.factory)
        self.attach(None)

Gst.init(None)

loop = GLib.MainLoop()

#import threading
#thread = threading.Thread(target=loop.run)
#thread.start()


#launch_string = f"videotestsrc is-live=true ! video/x-raw,format=I420,width=1280,height=720,framerate=15/1 ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay config-interval=1 name=pay0 pt=96 audiotestsrc is-live=true ! mulawenc ! rtppcmupay name=pay1"
#bin = Gst.parse_launch(launch_string)

#server = GstServer()
server = GstRtspServer.RTSPOnvifServer.new()
factory = GstRtspServer.RTSPOnvifMediaFactory.new()
factory.set_media_gtype(GstRtspServer.RTSPOnvifMedia)
factory.set_launch(launch_string)
#factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! fakesink async=false )")
#factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec ! wavenc ! filesink location=test.wav async=false )")
factory.set_backchannel_launch("( capsfilter caps=\"application/x-rtp,media=audio,payload=0,clock-rate=8000,encoding-name=PCMU\" name=depay_backchannel ! rtppcmudepay ! mulawdec ! audioconvert ! audioresample ! audio/x-raw,format=S16LE,channels=1,rate=8000 ! pulsesink device=\"BaresipMicrophone\" async=false )")
#factory.set_backchannel_bandwidth(2000)
factory.set_shared(False)
factory.set_latency(200)
factory.set_enable_rtcp(False)
#factory.set_protocols(GstRtsp.RTSPLowerTrans.TCP)
#factory.set_profiles(GstRtsp.RTSPProfile.AVP)
factory.connect("media-configure", media_configure)
server.get_mount_points().add_factory("/test", factory)

server.attach()

#import time
#while(True):
#    time.sleep(1)

loop.run()
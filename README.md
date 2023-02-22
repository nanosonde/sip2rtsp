# SIP2RTSP
A docker container that uses [baresip](https://github.com/baresip/baresip), [pulseaudio](https://www.freedesktop.org/wiki/Software/PulseAudio/) and [gstreamer RTSP server](https://gstreamer.freedesktop.org/documentation/gst-rtsp-server/rtsp-onvif-server.html?gi-language=python) to provide a solution that connects to a SIP peer (audio only) and a video camera to present an ONVIF profile T video doorbell with two-way audio support.

Please the following block diagram how this is achieved.


## Block diagram
Click [here](https://raw.githubusercontent.com/nanosonde/sip2rtsp/main/docs/sip2rtsp_block_diagram.svg) to open the block diagram in full screen.

![block_diagram](./docs/sip2rtsp_block_diagram.svg)


## Requirements

* docker (tested with 20.10.x on Ubuntu Jammy)

## Installation

Clone the GIT repo:
`git clone https://github.com/nanosonde/sip2rtsp.git`

Prepare configration file based on the example config file:
`cp config/config.yaml.example config/config.yaml`

Run the docker container with host networking mode:
`make run`


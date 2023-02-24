# SIP2RTSP
A docker container that uses [baresip](https://github.com/baresip/baresip), [pulseaudio](https://www.freedesktop.org/wiki/Software/PulseAudio/) and [gstreamer RTSP server](https://gstreamer.freedesktop.org/documentation/gst-rtsp-server/rtsp-onvif-server.html?gi-language=python) to provide a solution that connects to a SIP peer (audio only) and a video camera to present an ONVIF profile T video doorbell with two-way audio support.

Please the following block diagram how this is achieved.


## Block diagram
Click [here](https://raw.githubusercontent.com/nanosonde/sip2rtsp/main/docs/sip2rtsp_block_diagram.svg) to open the block diagram in full screen.

![block_diagram](./docs/sip2rtsp_block_diagram.svg)


## Requirements

* docker (tested with 20.10.x on Ubuntu Jammy)

## Installation

1. Clone the GIT repo:

  `git clone https://github.com/nanosonde/sip2rtsp.git`

2. Prepare configration file based on the example config file:

  `cp config/config.yaml.example config/config.yaml`

3. Run the docker container in host networking mode:

  `make run`

Please note that the generated docker image uses a custom build of gstreamer and pulseaudio from this repository: https://github.com/nanosonde/pulsegst
Building gstreamer and pulseaudio takes a long time. So building those is done in a separate dockerfile.

## Configuration

See the comments provided in config/config.yaml.example


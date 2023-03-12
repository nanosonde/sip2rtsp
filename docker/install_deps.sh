#!/bin/bash

set -euxo pipefail

apt-get -qq update

apt-get -qq install --no-install-recommends -y \
    apt-transport-https \
    gnupg \
    wget \
    procps \
    unzip locales tzdata libxml2 xz-utils \
    python3-pip \
    curl \
    jq

mkdir -p -m 600 /root/.gnupg

# enable non-free repo
#sed -i -e's/ main/ main contrib non-free/g' /etc/apt/sources.list

if [[ "${TARGETARCH}" == "amd64" ]]; then
    apt-get -qq install --no-install-recommends --no-install-suggests -y ffmpeg
fi

if [[ "${TARGETARCH}" == "arm" ]]; then
    # add raspberry pi repo
    mkdir -p -m 600 /root/.gnupg
    gpg --no-default-keyring --keyring /usr/share/keyrings/raspbian.gpg --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E
    echo "deb [signed-by=/usr/share/keyrings/raspbian.gpg] http://raspbian.raspberrypi.org/raspbian/ bookworm main contrib non-free rpi" | tee /etc/apt/sources.list.d/raspi.list
    apt-get -qq update
    apt-get -qq install --no-install-recommends --no-install-suggests -y ffmpeg
fi

# ffmpeg -> arm64
if [[ "${TARGETARCH}" == "arm64" ]]; then
    # add raspberry pi repo
    gpg --no-default-keyring --keyring /usr/share/keyrings/raspbian.gpg --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E
    echo "deb [signed-by=/usr/share/keyrings/raspbian.gpg] https://archive.raspberrypi.org/debian/ bookworm main" | tee /etc/apt/sources.list.d/raspi.list
    apt-get -qq update
    apt-get -qq install --no-install-recommends --no-install-suggests -y ffmpeg
fi

# Install baresip, pulseaudio deps and gstreamer
apt-get -qq install --no-install-recommends --no-install-suggests -y \
    libltdl7 \
    libtdb1 \
    baresip \
    baresip-core \
    baresip-gstreamer \
    baresip-x11 \
    python3-gi \
    libsoup2.4-1 \
    pulseaudio \
    pulseaudio-utils \
    gir1.2-gst-rtsp-server-1.0 \
    gir1.2-gstreamer-1.0 \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-rtp \
    gstreamer1.0-rtsp \
    gstreamer1.0-tools \
    gstreamer1.0-pulseaudio \
    gstreamer1.0-x

# Clean up

apt-get purge gnupg apt-transport-https wget curl xz-utils -y
apt-get clean autoclean -y
apt-get autoremove --purge -y
rm -rf /var/lib/apt/lists/*

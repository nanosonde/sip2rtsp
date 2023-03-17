#!/bin/bash

set -euxo pipefail

PULSEAUDIO_VERSION=16.1

apt-get update

# Install build dependencies for pulseaudio
apt-get -qq install -y \
    wget python3 python3-distutils \
    ninja-build build-essential pkgconf \
    libsndfile1-dev libltdl-dev libtdb-dev libglib2.0-dev libcap-dev

# Get and install pip and meson
wget -q https://bootstrap.pypa.io/get-pip.py -O get-pip.py
python3 get-pip.py "pip" --break-system-packages
pip install --break-system-packages meson

# Create a temporary directory for building pulseaudio, download the source code, extract it, and remove the archive
mkdir /tmp/pulseaudio
wget https://freedesktop.org/software/pulseaudio/releases/pulseaudio-${PULSEAUDIO_VERSION}.tar.gz
tar -zxf pulseaudio-${PULSEAUDIO_VERSION}.tar.gz -C /tmp/pulseaudio --strip-components=1
rm pulseaudio-${PULSEAUDIO_VERSION}.tar.gz

# Build and install pulseaudio
cd /tmp/pulseaudio
meson setup --prefix=/usr/local/pulseaudio \
    -Dman=false -Dtests=false -Ddoxygen=false \
    -Dudev=disabled -Ddbus=disabled \
    -Dx11=disabled -Dbluez5=disabled -Dgtk=disabled \
    -Dsystemd=disabled -Dalsa=disabled \
    -Djack=disabled -Dlirc=disabled \
    build

ninja -C build install

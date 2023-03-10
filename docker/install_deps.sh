#!/bin/bash

set -euxo pipefail

apt-get -qq update

apt-get -qq install --no-install-recommends -y \
    apt-transport-https \
    gnupg \
    wget \
    curl \
    procps \
    unzip locales tzdata libxml2 xz-utils \
    python3-pip

# add raspberry pi repo
mkdir -p -m 600 /root/.gnupg
gpg --no-default-keyring --keyring /usr/share/keyrings/raspbian.gpg --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E
echo "deb [signed-by=/usr/share/keyrings/raspbian.gpg] http://raspbian.raspberrypi.org/raspbian/ bullseye main contrib non-free rpi" | tee /etc/apt/sources.list.d/raspi.list

# enable non-free repo
sed -i -e's/ main/ main contrib non-free/g' /etc/apt/sources.list

apt-get -qq update

####
#### TODO: install packages per arch here
####

# Install nodejs 16.x
curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
apt-get -qq install --no-install-recommends --no-install-suggests -y nodejs

# Install baresip, pulseaudio deps and gstreamer
apt-get -qq install --no-install-recommends --no-install-suggests -y \
    libltdl7 \
    libtdb1 \
    baresip \
    baresip-core \
    baresip-gstreamer \
    baresip-x11 \
    python3-gi \
    libsoup2.4-1

# Clean up

apt-get purge gnupg apt-transport-https wget curl xz-utils -y
apt-get clean autoclean -y
apt-get autoremove --purge -y
rm -rf /var/lib/apt/lists/*

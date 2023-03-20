#!/bin/bash

set -euxo pipefail

LIBRE_VERSION=2.12.0
LIBREM_VERSION=2.12.0
BARESIP_VERSION=2.12.0

echo "deb-src http://ftp.de.debian.org/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list.d/sources-src.list
apt-get update

# Install build dependencies for baresip
apt-get -qq install -y \
    wget \
    build-essential \
    pkgconf \
    cmake

apt-get -qq build-dep -y baresip
    
# Create a temporary directory for building libre, download the source code, extract it, and remove the archive
mkdir /tmp/libre
wget https://github.com/baresip/re/archive/refs/tags/v${LIBRE_VERSION}.tar.gz
tar -zxf v${LIBRE_VERSION}.tar.gz -C /tmp/libre --strip-components=1
rm v${LIBRE_VERSION}.tar.gz

# Create a temporary directory for building librem, download the source code, extract it, and remove the archive
mkdir /tmp/librem
wget https://github.com/baresip/rem/archive/refs/tags/v${LIBREM_VERSION}.tar.gz
tar -zxf v${LIBREM_VERSION}.tar.gz -C /tmp/librem --strip-components=1
rm v${LIBREM_VERSION}.tar.gz

# Create a temporary directory for building baresip, download the source code, extract it, and remove the archive
mkdir /tmp/baresip
wget https://github.com/baresip/baresip/archive/refs/tags/v${BARESIP_VERSION}.tar.gz
tar -zxf v${BARESIP_VERSION}.tar.gz -C /tmp/baresip --strip-components=1
rm v${BARESIP_VERSION}.tar.gz

mkdir -p /usr/local/baresip

# Build and install libre
cd /tmp/libre
cmake -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=/usr/
cmake --build build -j
cmake --install build --prefix dist && cp -a dist/* /usr/ && cp -a dist/* /usr/local/baresip/

# Build and install librem
cd /tmp/librem
cmake -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=/usr/
cmake --build build -j
cmake --install build --prefix dist && cp -a dist/* /usr/ && cp -a dist/* /usr/local/baresip/

# Build and install baresip
cd /tmp/baresip
cmake -B build -DSTATIC=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=/usr/
cmake --build build -j
cmake --install build --prefix dist && cp -a dist/* /usr/ && cp -a dist/* /usr/local/baresip/

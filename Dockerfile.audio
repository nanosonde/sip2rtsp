# syntax=docker/dockerfile:1.2

# https://askubuntu.com/questions/972516/debian-frontend-environment-variable
ARG DEBIAN_FRONTEND=noninteractive

FROM debian:11 AS base

# Download and build pulseaudio
FROM base AS pulseaudio
ARG DEBIAN_FRONTEND
ARG PULSEAUDIO_VERSION=16.1

# Install pulseaudio
RUN apt-get -qq update \
    && apt-get -qq install -y wget python3 python3-distutils \
                              ninja-build build-essential pkgconf \
                              libsndfile1-dev libltdl-dev libtdb-dev libglib2.0-dev libcap-dev \
    && wget -q https://bootstrap.pypa.io/get-pip.py -O get-pip.py \
    && python3 get-pip.py "pip" \
    && pip install meson \
    && mkdir /tmp/pulseaudio \
    && wget https://freedesktop.org/software/pulseaudio/releases/pulseaudio-${PULSEAUDIO_VERSION}.tar.gz \
    && tar -zxf pulseaudio-${PULSEAUDIO_VERSION}.tar.gz -C /tmp/pulseaudio --strip-components=1 \
    && rm pulseaudio-${PULSEAUDIO_VERSION}.tar.gz

WORKDIR /tmp/pulseaudio

RUN meson setup --prefix=/usr/local/pulseaudio \
    -Dman=false -Dtests=false -Ddoxygen=false \
    -Dudev=disabled -Ddbus=disabled \
    -Dx11=disabled -Dbluez5=disabled -Dgtk=disabled \
    -Dsystemd=disabled -Dalsa=disabled \
    -Djack=disabled -Dlirc=disabled \
    build \
    && ninja -C build install \
    && ldconfig

# Download and build gstreamer
FROM base AS gstreamer
ARG DEBIAN_FRONTEND
ARG GSTREAMER_VERSION=1.21.3

COPY --from=pulseaudio /usr/local/pulseaudio/ /usr/local/

# Install gstreamer
RUN apt-get -qq update \
    && apt-get -qq install -y wget git python3 python3-distutils python3-gi python-gi-dev \
                              ninja-build build-essential pkgconf flex bison \
                              gobject-introspection libgirepository1.0-dev libunwind-dev libdw-dev \
                              gir1.2-glib-2.0 gir1.2-freedesktop zlib1g-dev libglib2.0-dev libsoup2.4-dev \
    && wget -q https://bootstrap.pypa.io/get-pip.py -O get-pip.py \
    && python3 get-pip.py "pip" \
    && pip install meson \
    && mkdir /tmp/gstreamer \
    && wget https://gitlab.freedesktop.org/gstreamer/gstreamer/-/archive/${GSTREAMER_VERSION}/gstreamer-${GSTREAMER_VERSION}.tar.gz \
    && tar -zxf gstreamer-${GSTREAMER_VERSION}.tar.gz -C /tmp/gstreamer --strip-components=1 \
    && rm gstreamer-${GSTREAMER_VERSION}.tar.gz

WORKDIR /tmp/gstreamer

RUN meson setup --prefix=/usr/local/gstreamer \
    -Dgood=enabled -Dbad=enabled -Dugly=enabled -Dgpl=enabled -Dintrospection=enabled \
    -Dgst-plugins-ugly:x264=enabled \
    -Dgst-plugins-good:pulse=enabled \
    -Dgst-plugins-good:soup=enabled \
    build \
    && ninja -C build install \
    && ldconfig

FROM scratch
COPY --from=pulseaudio /usr/local/pulseaudio/ /usr/local/pulseaudio/
COPY --from=gstreamer /usr/local/gstreamer/ /usr/local/gstreamer/


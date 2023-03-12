# syntax=docker/dockerfile:1.2

# https://askubuntu.com/questions/972516/debian-frontend-environment-variable
ARG DEBIAN_FRONTEND=noninteractive

FROM debian:bookworm AS base

FROM --platform=linux/amd64 debian:bookworm AS base_amd64

FROM debian:bookworm-slim AS slim-base

FROM slim-base AS wget
ARG DEBIAN_FRONTEND
RUN apt-get update \
    && apt-get install -y wget xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /rootfs

FROM wget AS s6-overlay
ARG TARGETARCH
RUN --mount=type=bind,source=docker/install_s6_overlay.sh,target=/deps/install_s6_overlay.sh \
    /deps/install_s6_overlay.sh


FROM base AS wheels
ARG DEBIAN_FRONTEND
ARG TARGETARCH

# Use a separate container to build wheels to prevent build dependencies in final image
RUN apt-get -qq update \
    && apt-get -qq install -y \
    apt-transport-https \
    gnupg \
    wget \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E \
    && echo "deb http://raspbian.raspberrypi.org/raspbian/ bookworm main contrib non-free rpi" | tee /etc/apt/sources.list.d/raspi.list \
    && apt-get -qq update \
    && apt-get -qq install -y \
    python3 \
    python3-dev \
    wget \
    build-essential cmake git pkg-config libssl-dev

RUN wget -q https://bootstrap.pypa.io/get-pip.py -O get-pip.py \
    && python3 get-pip.py "pip" --break-system-packages

RUN if [ "${TARGETARCH}" = "arm" ]; \
    then echo "[global]" > /etc/pip.conf \
    && echo "extra-index-url=https://www.piwheels.org/simple" >> /etc/pip.conf; \
    fi

COPY requirements.txt /requirements.txt
RUN pip3 install --break-system-packages -r requirements.txt

COPY requirements-wheels.txt /requirements-wheels.txt
RUN pip3 wheel --wheel-dir=/wheels -r requirements-wheels.txt

# Collect deps in a single layer
FROM scratch AS deps-rootfs

#COPY --from=pulsegstimage /usr/local/pulseaudio/ /usr/local/pulseaudio/
#COPY --from=pulsegstimage /usr/local/gstreamer/ /usr/local/gstreamer/
COPY --from=s6-overlay /rootfs/ /
COPY docker/rootfs/ /


# The deps (python, s6-overlay, etc)
FROM slim-base AS deps
ARG TARGETARCH

ARG DEBIAN_FRONTEND
# http://stackoverflow.com/questions/48162574/ddg#49462622
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

#ENV PATH="/usr/local/pulseaudio/bin:/usr/local/gstreamer/bin:${PATH}"
#ENV GI_TYPELIB_PATH="/usr/local/gstreamer/lib/x86_64-linux-gnu/girepository-1.0/"

# Install dependencies
RUN --mount=type=bind,source=docker/install_deps.sh,target=/deps/install_deps.sh \
    /deps/install_deps.sh

RUN --mount=type=bind,from=wheels,source=/wheels,target=/deps/wheels \
    pip3 install --break-system-packages -U /deps/wheels/*.whl

COPY --from=deps-rootfs / /

# make sure the dynlib loader finds our libs from /etc/ld.so.conf.d
RUN ldconfig

#EXPOSE 8554
#EXPOSE 8555/tcp 8555/udp

# Configure logging to prepend timestamps, log to stdout, keep 0 archives and rotate on 10MB
ENV S6_LOGGING_SCRIPT="T 1 n0 s10000000 T"

ENTRYPOINT ["/init"]
CMD []

# sip2rtsp deps with Node.js and NPM for devcontainer
FROM deps AS devcontainer

# Do not start the actual sip2rtsp service on devcontainer as it will be started by VSCode
# But start a fake services for simulating the logs
COPY docker/fake_sip2rtsp_run /etc/s6-overlay/s6-rc.d/sip2rtsp/run

WORKDIR /workspace/sip2rtsp

RUN apt-get update \
    && apt-get install make -y \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=./requirements-dev.txt,target=/workspace/sip2rtsp/requirements-dev.txt \
    pip3 install -r requirements-dev.txt

CMD ["sleep", "infinity"]

# Collect final files in a single layer
FROM scratch AS rootfs

WORKDIR /opt/sip2rtsp/
COPY sip2rtsp sip2rtsp/
COPY pyonvifsrv pyonvifsrv/

# sip2rtsp final container
FROM deps as sip2rtsp

WORKDIR /opt/sip2rtsp/
COPY --from=rootfs / /

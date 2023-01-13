# syntax=docker/dockerfile:1.2

# https://askubuntu.com/questions/972516/debian-frontend-environment-variable
ARG DEBIAN_FRONTEND=noninteractive

FROM debian:11 AS base

FROM --platform=linux/amd64 debian:11 AS base_amd64

FROM debian:11-slim AS slim-base

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
    && echo "deb http://raspbian.raspberrypi.org/raspbian/ bullseye main contrib non-free rpi" | tee /etc/apt/sources.list.d/raspi.list \
    && apt-get -qq update \
    && apt-get -qq install -y \
    python3 \
    python3-dev \
    wget \
    build-essential cmake git pkg-config libssl-dev

RUN wget -q https://bootstrap.pypa.io/get-pip.py -O get-pip.py \
    && python3 get-pip.py "pip"

RUN if [ "${TARGETARCH}" = "arm" ]; \
    then echo "[global]" > /etc/pip.conf \
    && echo "extra-index-url=https://www.piwheels.org/simple" >> /etc/pip.conf; \
    fi

COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

COPY requirements-wheels.txt /requirements-wheels.txt
RUN pip3 wheel --wheel-dir=/wheels -r requirements-wheels.txt


# Collect deps in a single layer
FROM scratch AS deps-rootfs
COPY --from=sip2rtsp-audio:latest /usr/local/pulseaudio/ /usr/local/pulseaudio/
COPY --from=sip2rtsp-audio:latest /usr/local/gstreamer/ /usr/local/gstreamer/
COPY --from=s6-overlay /rootfs/ /
COPY docker/rootfs/ /


# The deps (python, s6-overlay, etc)
FROM slim-base AS deps
ARG TARGETARCH

ARG DEBIAN_FRONTEND
# http://stackoverflow.com/questions/48162574/ddg#49462622
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

ENV PATH="/usr/local/pulseaudio/bin:/usr/local/gstreamer/bin:${PATH}"
ENV GI_TYPELIB_PATH="/usr/local/gstreamer/lib/x86_64-linux-gnu/girepository-1.0/"

# Install dependencies
RUN --mount=type=bind,source=docker/install_deps.sh,target=/deps/install_deps.sh \
    /deps/install_deps.sh

RUN --mount=type=bind,from=wheels,source=/wheels,target=/deps/wheels \
    pip3 install -U /deps/wheels/*.whl

COPY --from=deps-rootfs / /

RUN echo "/usr/local/gstreamer/lib/x86_64-linux-gnu" > /etc/ld.so.conf.d/gstreamer.conf \
    && ldconfig

#EXPOSE 8554
#EXPOSE 8555

# Fails if cont-init.d fails
ENV S6_BEHAVIOUR_IF_STAGE2_FAILS=2
# Wait indefinitely for cont-init.d to finish before starting services
ENV S6_CMD_WAIT_FOR_SERVICES=1
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0
# Give services (including Frigate) 30 seconds to stop before killing them
# But this is not working currently because of:
# https://github.com/just-containers/s6-overlay/issues/503
ENV S6_SERVICES_GRACETIME=30000
# Configure logging to prepend timestamps, log to stdout, keep 0 archives and rotate on 10MB
ENV S6_LOGGING_SCRIPT="T 1 n0 s10000000 T"
# TODO: remove after a new version of s6-overlay is released. See:
# https://github.com/just-containers/s6-overlay/issues/460#issuecomment-1327127006
ENV S6_SERVICES_READYTIME=50

ENTRYPOINT ["/init"]
CMD []

# sip2rtsp deps with Node.js and NPM for devcontainer
FROM deps AS devcontainer

# Do not start the actual sip2rtsp and onvif-server services on devcontainer as it will be started by VSCode
# But start a fake services for simulating the logs
COPY docker/fake_sip2rtsp_run /etc/services.d/sip2rtsp/run
COPY docker/fake_onvif-server_run /etc/services.d/onvif-server/run

# Install Node 16
RUN apt-get update \
    && apt-get install wget -y \
    && wget -qO- https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g npm@9

WORKDIR /workspace/sip2rtsp

RUN apt-get update \
    && apt-get install make -y \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=./requirements-dev.txt,target=/workspace/sip2rtsp/requirements-dev.txt \
    pip3 install -r requirements-dev.txt

CMD ["sleep", "infinity"]

# ONVIF server build
# force this to run on amd64 because QEMU is painfully slow
FROM --platform=linux/amd64 node:16 AS onvif-server-build

WORKDIR /work
COPY onvif-server/package.json onvif-server/package-lock.json ./
RUN npm install

COPY onvif-server/ ./
RUN npm run build
#RUN npm run build \
#    && mv dist/BASE_PATH/monacoeditorwork/* dist/assets/ \
#    && rm -rf dist/BASE_PATH

# Collect final files in a single layer
FROM scratch AS rootfs

WORKDIR /opt/sip2rtsp/
COPY sip2rtsp sip2rtsp/
COPY --from=onvif-server-build /work/dist/ onvif-server/
COPY --from=onvif-server-build /work/node_modules/ onvif-server/node_modules/

# sip2rtsp final container
FROM deps

WORKDIR /opt/sip2rtsp/
COPY --from=rootfs / /

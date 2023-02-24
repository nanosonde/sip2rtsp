default_target: local

COMMIT_HASH := $(shell git log -1 --pretty=format:"%h"|tail -1)
VERSION = 0.0.1
IMAGE_REPO ?= ghcr.io/nanosonde/sip2rtsp
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
PULSEGST_IMAGE = ghcr.io/nanosonde/pulsegst:main-60fc993
PULSEGST_IMAGE_AMD64 = ghcr.io/nanosonde/pulsegst:main-fc3b544@sha256:e69b7f64c92e1c1459d491d39f69b08f1ee3b0b2cc49c14839c7d2b1e03eb519
PULSEGST_IMAGE_ARM64 = ghcr.io/nanosonde/pulsegst:main-fc3b544@sha256:dece2d9fd7d3c676ffb59b6d54cf9ea62ddca8b420e3734598f8eec56974de7a

version:
	echo 'VERSION = "$(VERSION)-$(COMMIT_HASH)"' > sip2rtsp/version.py

local: version
	docker buildx build --build-arg PULSEGST_IMAGE=pulsegst:latest --target=sip2rtsp --tag sip2rtsp:latest .

amd64:
	docker buildx build --platform linux/amd64 --build-arg PULSEGST_IMAGE=$(PULSEGST_IMAGE_AMD64) --target=sip2rtsp --tag $(IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

arm64:
	docker buildx build --platform linux/arm64 --build-arg PULSEGST_IMAGE=$(PULSEGST_IMAGE_ARM64) --target=sip2rtsp --tag $(IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

#armv7:
#	docker buildx build --platform linux/arm/v7 --build-arg PULSEGST_IMAGE=$(PULSEGST_IMAGE_ARMv7) --target=sip2rtsp --tag $(IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

#build: version amd64 arm64 armv7
build: version amd64 arm64
#	docker buildx build --platform linux/arm/v7,linux/arm64,linux/amd64 --build-arg PULSEGST_IMAGE=$(PULSEGST_IMAGE) --target=sip2rtsp --tag $(IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .
	docker buildx build --platform linux/arm64,linux/amd64 --build-arg PULSEGST_IMAGE=$(PULSEGST_IMAGE) --target=sip2rtsp --tag $(IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

push: build
#	docker buildx build --push --platform linux/arm/v7,linux/arm64,linux/amd64 --target=sip2rtsp --tag $(IMAGE_REPO):${GITHUB_REF_NAME}-$(COMMIT_HASH) .
	docker buildx build --push --platform linux/arm64,linux/amd64 --target=sip2rtsp --tag $(IMAGE_REPO):${GITHUB_REF_NAME}-$(COMMIT_HASH) .

run: local
	docker run --rm --network host --volume=${PWD}/config/config.yml:/config/config.yml --name sip2rtsp sip2rtsp:latest

run_shell: local
	docker run --rm --network host --volume=${PWD}/config/config.yml:/config/config.yml --name sip2rtsp-shell -it sip2rtsp:latest /bin/bash

run_tests: local
	docker run --rm --workdir=/opt/sip2rtsp --entrypoint= sip2rtsp:latest python3 -u -m unittest
	docker run --rm --workdir=/opt/sip2rtsp --entrypoint= sip2rtsp:latest python3 -u -m mypy --config-file sip2rtsp/mypy.ini sip2rtsp

prune_build_cache:
	docker builder prune

.PHONY: run_tests

# FFMPEG gstreamer broken for armv7: why does ffmpeg on armv7 try to use neon instructions?
#0 15417.9 cc -Isubprojects/FFmpeg/libavutil-static.a.p -Isubprojects/FFmpeg -I../subprojects/FFmpeg -fdiagnostics-color=always -D_FILE_OFFSET_BITS=64 -Wall -Winvalid-pch -std=c99 -O2 -g -D_ISOC99_SOURCE -D_GNU_SOURCE -D_LARGEFILE_SOURCE -DPIC -Wno-parentheses -Wno-pointer-sign -Wno-switch -Wno-format-truncation -Wno-deprecated-declarations -Wno-unused-function -Wno-maybe-uninitialized -Wno-discarded-qualifiers -Wno-unused-variable -Wno-bool-operation -Wno-incompatible-pointer-types -Wno-address -D_POSIX_C_SOURCE=200112 -D_XOPEN_SOURCE=600 -mthumb -fPIC -pthread -DHAVE_AV_CONFIG_H -DBUILDING_avutil -MD -MQ subprojects/FFmpeg/libavutil-static.a.p/libavutil_arm_float_dsp_neon.S.o -MF subprojects/FFmpeg/libavutil-static.a.p/libavutil_arm_float_dsp_neon.S.o.d -o subprojects/FFmpeg/libavutil-static.a.p/libavutil_arm_float_dsp_neon.S.o -c ../subprojects/FFmpeg/libavutil/arm/float_dsp_neon.S
#0 15417.9 ../subprojects/FFmpeg/libavutil/arm/float_dsp_neon.S: Assembler messages:
#0 15417.9 ../subprojects/FFmpeg/libavutil/arm/float_dsp_neon.S:29: Error: selected FPU does not support instruction -- `vmul.f32 q8,q0,q2'
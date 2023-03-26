default_target: local

COMMIT_HASH := $(shell git log -1 --pretty=format:"%h"|tail -1)
REF_NAME := $(shell git symbolic-ref --short HEAD)
VERSION = 0.0.1
GHCR_IMAGE_REPO ?= ghcr.io/nanosonde/sip2rtsp
DOCKERHUB_IMAGE_REPO ?= nanosonde/sip2rtsp
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

version:
	echo 'VERSION = "$(VERSION)-$(COMMIT_HASH)"' > sip2rtsp/version.py

local: version
	docker buildx build --target=sip2rtsp --tag sip2rtsp:latest --load .

amd64: version
	docker buildx build --platform linux/amd64 --target=sip2rtsp --tag $(GHCR_IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

arm64: version
	docker buildx build --platform linux/arm64 --target=sip2rtsp --tag $(GHCR_IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

armv7: version
	docker buildx build --platform linux/arm/v7 --target=sip2rtsp --tag $(GHCR_IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

build: version
	docker buildx build --platform linux/arm/v7,linux/arm64,linux/amd64 --target=sip2rtsp --tag $(GHCR_IMAGE_REPO):$(VERSION)-$(COMMIT_HASH) .

push_ghcr:
	docker buildx build --push --platform linux/arm/v7,linux/arm64,linux/amd64 --target=sip2rtsp --tag $(GHCR_IMAGE_REPO):${REF_NAME}-$(COMMIT_HASH) .

push_docker:
	docker buildx build --push --platform linux/arm/v7,linux/arm64,linux/amd64 --target=sip2rtsp --tag $(DOCKERHUB_IMAGE_REPO):$(REF_NAME)-$(COMMIT_HASH) .

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

from __future__ import annotations

import json
import logging
import os
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Extra, Field, validator, parse_obj_as
from pydantic.fields import PrivateAttr

from sip2rtsp.const import (
    YAML_EXT,
)
from sip2rtsp.util import (
    load_config_with_no_duplicates,
)
from sip2rtsp.version import VERSION

logger = logging.getLogger(__name__)

SIP2RTSP_ENV_VARS = {k: v for k, v in os.environ.items() if k.startswith("SIP2RTSP_")}


class Sip2RtspBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid


class LogLevelEnum(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class LoggerConfig(Sip2RtspBaseModel):
    default: LogLevelEnum = Field(
        default=LogLevelEnum.info, title="Default logging level."
    )
    logs: Dict[str, LogLevelEnum] = Field(
        default_factory=dict, title="Log level for specified processes."
    )


class RtspServerConfig(Sip2RtspBaseModel):
    launch_string: str = Field(
        default="", title="GStreamer RTSP server: launch string."
    )
    backchannel_launch_string: str = Field(
        default="", title="GStreamer RTSP server: backchannel launch string."
    )
    port: int = Field(
        default=8554, title="GStreamer RTSP server: TCP port to listen on."
    )
    mount_point: str = Field(default="", title="GStreamer RTSP server: mount point.")
    latency: int = Field(default=200, title="GStreamer RTSP server: latency.")
    enable_rtcp: bool = Field(
        default=False, title="GStreamer RTSP server: enable RTCP."
    )


class SipConfig(Sip2RtspBaseModel):
    remote_uri: str = Field(
        default="sip:11@10.10.10.80", title="SIP doorbell: remote URI to dial."
    )

class CameraConfig(Sip2RtspBaseModel):
    name: str = Field(
        default="sip2rtsp-cam", title="ONVIF server: Camera name to report"
    )
    location: str = Field(
        default="sip2rtsp-location", title="ONVIF server: Camera location to report"
    )
    width: int = Field(default=1920, title="ONVIF server: Camera width to report")
    height: int = Field(default=1080, title="ONVIF server: Camera height to report")
    fps: int = Field(default=30, title="ONVIF server: Camera fps to report")
    bitrate: int = Field(default=1000, title="ONVIF server: Camera bitrate to report")

class OnvifConfig(Sip2RtspBaseModel):
    server_address: str = Field(
        default="10.10.10.70", title="ONVIF server: address to advertise."
    )
    server_port: int = Field(default=10101, title="ONVIF server: port to advertise.")
    hostname: str = Field(
        default="sip2rtsp-cam", title="ONVIF server: hostname to report"
    )
    camera: CameraConfig = Field(default_factory=CameraConfig, title="ONVIF camera configuration")

class Sip2RtspConfig(Sip2RtspBaseModel):
    environment_vars: Dict[str, str] = Field(
        default_factory=dict, title="sip2rtsp environment variables."
    )
    logger: LoggerConfig = Field(
        default_factory=LoggerConfig, title="Logging configuration."
    )

    rtsp_server: RtspServerConfig = Field(
        default_factory=RtspServerConfig, title="GStreamer RTSP server configuration."
    )

    sip: SipConfig = Field(default_factory=SipConfig, title="SIP configuration.")

    onvif: OnvifConfig = Field(
        default_factory=OnvifConfig, title="ONVIF configuration."
    )

    @property
    def runtime_config(self) -> Sip2RtspConfig:
        """Merge config with globals."""
        config = self.copy(deep=True)
        print(config)
        return config

    @classmethod
    def parse_file(cls, config_file):
        with open(config_file) as f:
            raw_config = f.read()

        if config_file.endswith(YAML_EXT):
            config = load_config_with_no_duplicates(raw_config)
        elif config_file.endswith(".json"):
            config = json.loads(raw_config)

        return cls.parse_obj(config)

    @classmethod
    def parse_raw(cls, raw_config):
        config = load_config_with_no_duplicates(raw_config)
        return cls.parse_obj(config)

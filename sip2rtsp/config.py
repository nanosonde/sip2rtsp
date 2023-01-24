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


class Sip2RtspConfig(Sip2RtspBaseModel):
    environment_vars: Dict[str, str] = Field(
        default_factory=dict, title="sip2rtsp environment variables."
    )
    logger: LoggerConfig = Field(
        default_factory=LoggerConfig, title="Logging configuration."
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

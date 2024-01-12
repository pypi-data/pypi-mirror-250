#!/usr/bin/env python3
"""
 Configuration class, used as a base for system configurations

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

import warnings
from pathlib import Path
from typing import Dict, Union

import yaml  # type: ignore
from pydantic import BaseModel


class Config(BaseModel, validate_assignment=True):
    """Base configuration class"""

    def from_yaml(self, file_path: Union[str, Path]):
        warnings.warn(
            "Config.from_yaml is deprecated, use Config.update_from_yaml instead",
            DeprecationWarning,
        )
        self.update_from_yaml(file_path)

    def update_from_yaml(self, file_path: Union[str, Path]):
        """Update configuration from a YAML file"""

        with open(file_path, "r", encoding="utf8") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        self.update(yaml_data)

    def update(self, data: Dict):
        """Update configuration from a dictionary"""

        for key, value in data.items():
            setattr(self, key, value)

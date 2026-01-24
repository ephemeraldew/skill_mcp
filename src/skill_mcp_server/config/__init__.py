# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Configuration management for Skill MCP Server."""

from .settings import Settings
from .defaults import (
    DEFAULT_SKILLS_DIR,
    DEFAULT_WORKSPACE_DIR,
    ALLOWED_FILE_EXTENSIONS,
    ALLOWED_SCRIPT_EXTENSIONS,
    MAX_FILE_SIZE,
    MAX_READ_SIZE,
    SCRIPT_TIMEOUT,
)
from .loader import load_config

__all__ = [
    "Settings",
    "load_config",
    "DEFAULT_SKILLS_DIR",
    "DEFAULT_WORKSPACE_DIR",
    "ALLOWED_FILE_EXTENSIONS",
    "ALLOWED_SCRIPT_EXTENSIONS",
    "MAX_FILE_SIZE",
    "MAX_READ_SIZE",
    "SCRIPT_TIMEOUT",
]

# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Logging configuration for Skill MCP Server."""

from __future__ import annotations

import logging
import os
import sys
from typing import Optional

# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Package logger name
LOGGER_NAME = "skill_mcp_server"

# Environment variable for log level override
LOG_LEVEL_ENV = "SKILL_MCP_LOG_LEVEL"


def setup_logging(
    verbose: bool = False,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Configure logging for the application.

    Args:
        verbose: If True, set level to DEBUG; otherwise INFO.
        log_format: Custom log format string.

    Returns:
        Configured root logger for the package.

    Environment variables:
        SKILL_MCP_LOG_LEVEL: Override log level (DEBUG, INFO, WARNING, ERROR, CRITICAL, SILENT)
                            Use SILENT to disable all logging output.
    """
    # Check environment variable for log level override
    env_level = os.environ.get(LOG_LEVEL_ENV, "").upper()

    # Handle SILENT mode - disable all logging output
    if env_level == "SILENT":
        # Don't configure any handlers, just return a disabled logger
        logging.disable(logging.CRITICAL)
        logger = logging.getLogger(LOGGER_NAME)
        logger.addHandler(logging.NullHandler())
        return logger

    if env_level and hasattr(logging, env_level):
        level = getattr(logging, env_level)
    else:
        level = logging.DEBUG if verbose else logging.INFO

    fmt = log_format or DEFAULT_FORMAT

    # Configure the root logger
    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    # Get and configure our package logger
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name. If None, returns the package root logger.
              If provided, creates a child logger under the package namespace.

    Returns:
        Logger instance.
    """
    # Check for silent mode
    if os.environ.get(LOG_LEVEL_ENV, "").upper() == "SILENT":
        logging.disable(logging.CRITICAL)

    if name is None:
        return logging.getLogger(LOGGER_NAME)

    # Create child logger under our package namespace
    return logging.getLogger(f"{LOGGER_NAME}.{name}")

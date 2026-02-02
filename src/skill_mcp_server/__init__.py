# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""
Skill MCP Server - Turn any AI agent into a specialist.

A Model Context Protocol (MCP) server that enables AI agents to use
modular skills. Simply drop skill folders into the skills directory,
and your agent gains new capabilities instantly.

Example:
    >>> from skill_mcp_server import create_server
    >>> from pathlib import Path
    >>> import asyncio
    >>>
    >>> server = create_server(
    ...     skills_dir=Path("./skills"),
    ...     workspace_dir=Path("./workspace"),
    ... )
    >>> asyncio.run(server.run())
"""

# Early silent mode check - must happen before any logging
import logging as _logging
import os as _os

if _os.environ.get("SKILL_MCP_LOG_LEVEL", "").upper() == "SILENT":
    _logging.disable(_logging.CRITICAL)

from .config.settings import Settings
from .core.server import SkillMCPServer, create_server
from .skill.manager import SkillManager
from .skill.models import SkillInfo

__version__ = "0.1.0"
__author__ = "Skill MCP Server Contributors"
__license__ = "MIT"

__all__ = [
    "SkillMCPServer",
    "create_server",
    "SkillManager",
    "SkillInfo",
    "Settings",
    "__version__",
]

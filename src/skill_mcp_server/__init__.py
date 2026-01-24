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

from .core.server import SkillMCPServer, create_server
from .skill.manager import SkillManager
from .skill.models import SkillInfo
from .config.settings import Settings

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

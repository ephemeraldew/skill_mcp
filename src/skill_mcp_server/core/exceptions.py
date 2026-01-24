# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Custom exceptions for Skill MCP Server."""


class ServerError(Exception):
    """Base exception for server errors."""

    pass


class ToolNotFoundError(ServerError):
    """Raised when a requested tool is not found."""

    def __init__(self, tool_name: str) -> None:
        self.tool_name = tool_name
        super().__init__(f"Tool not found: {tool_name}")


class ConfigurationError(ServerError):
    """Raised when there's a configuration problem."""

    pass


class InitializationError(ServerError):
    """Raised when server initialization fails."""

    pass

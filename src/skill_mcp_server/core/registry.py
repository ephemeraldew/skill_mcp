# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Tool registry for managing MCP tools."""

from __future__ import annotations

from typing import Optional

from mcp.types import Tool

from ..tools.base import BaseTool
from ..utils.logging import get_logger
from .exceptions import ToolNotFoundError

logger = get_logger("core.registry")


class ToolRegistry:
    """Registry for MCP tools.

    Manages tool registration, lookup, and provides
    MCP-compatible tool definitions.
    """

    def __init__(self) -> None:
        """Initialize the registry."""
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool.

        Args:
            tool: Tool instance to register.
        """
        if tool.name in self._tools:
            logger.warning(f"Overwriting existing tool: {tool.name}")

        self._tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name}")

    def register_many(self, tools: list[BaseTool]) -> None:
        """Register multiple tools.

        Args:
            tools: List of tool instances.
        """
        for tool in tools:
            self.register(tool)

    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name.

        Args:
            name: Tool name.

        Returns:
            Tool instance or None if not found.
        """
        return self._tools.get(name)

    def get_or_raise(self, name: str) -> BaseTool:
        """Get a tool by name, raising if not found.

        Args:
            name: Tool name.

        Returns:
            Tool instance.

        Raises:
            ToolNotFoundError: If tool is not registered.
        """
        tool = self.get(name)
        if tool is None:
            raise ToolNotFoundError(name)
        return tool

    def list_tools(self) -> list[Tool]:
        """Get MCP Tool definitions for all registered tools.

        Returns:
            List of MCP Tool objects.
        """
        return [tool.to_mcp_tool() for tool in self._tools.values()]

    def names(self) -> list[str]:
        """Get all registered tool names.

        Returns:
            List of tool names.
        """
        return list(self._tools.keys())

    def count(self) -> int:
        """Get the number of registered tools.

        Returns:
            Number of tools.
        """
        return len(self._tools)

    def clear(self) -> None:
        """Remove all registered tools."""
        self._tools.clear()

    def __contains__(self, name: str) -> bool:
        """Check if a tool is registered.

        Args:
            name: Tool name.

        Returns:
            True if tool is registered.
        """
        return name in self._tools

    def __len__(self) -> int:
        """Get the number of registered tools."""
        return len(self._tools)

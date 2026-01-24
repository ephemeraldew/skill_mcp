# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Base tool interface for MCP tools."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from mcp.types import Tool


class ToolError(Exception):
    """Raised when a tool execution fails."""

    pass


class BaseTool(ABC):
    """Abstract base class for MCP tools.

    Each tool implementation should:
    1. Define its name and description
    2. Define its input schema
    3. Implement the execute method
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the tool name.

        Returns:
            Unique tool identifier.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get the tool description.

        Returns:
            Human-readable description of what the tool does.
        """
        pass

    @property
    @abstractmethod
    def input_schema(self) -> dict[str, Any]:
        """Get the JSON schema for tool input.

        Returns:
            JSON Schema describing the tool's parameters.
        """
        pass

    @abstractmethod
    def execute(self, **kwargs: Any) -> str:
        """Execute the tool with the given arguments.

        Args:
            **kwargs: Tool-specific arguments.

        Returns:
            Result string to return to the client.

        Raises:
            ToolError: If execution fails.
        """
        pass

    def to_mcp_tool(self) -> Tool:
        """Convert to MCP Tool object.

        Returns:
            MCP Tool definition.
        """
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.input_schema,
        )

# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Main MCP Server implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from ..config.settings import Settings
from ..config.loader import load_config
from ..security.file_validator import FileValidator
from ..skill.manager import SkillManager
from ..tools.skill_loader import SkillLoaderTool
from ..tools.skill_lister import SkillListerTool
from ..tools.resource_reader import ResourceReaderTool
from ..tools.script_executor import ScriptExecutorTool
from ..tools.file_reader import FileReaderTool
from ..tools.file_writer import FileWriterTool
from ..tools.file_editor import FileEditorTool
from ..utils.logging import get_logger, setup_logging
from .registry import ToolRegistry
from .exceptions import ToolNotFoundError

logger = get_logger("core.server")


class SkillMCPServer:
    """Skill MCP Server - exposes skills as MCP tools.

    This is the main entry point for the MCP server. It coordinates
    all components and handles the MCP protocol.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize the server.

        Args:
            settings: Server configuration.
        """
        self.settings = settings

        # Ensure directories exist
        self.settings.ensure_directories()

        # Initialize components
        self._init_validators()
        self._init_skill_manager()
        self._init_tools()
        self._init_mcp_server()

        logger.info(f"Skills directory: {self.settings.skills_dir}")
        logger.info(f"Workspace directory: {self.settings.workspace_dir}")

    def _init_validators(self) -> None:
        """Initialize security validators."""
        self.file_validator = FileValidator(
            allowed_extensions=self.settings.allowed_file_extensions,
            allowed_script_extensions=self.settings.allowed_script_extensions,
            max_file_size=self.settings.max_file_size,
            max_read_size=self.settings.max_read_size,
        )

    def _init_skill_manager(self) -> None:
        """Initialize the skill manager."""
        self.skill_manager = SkillManager(
            skill_dirs=[self.settings.skills_dir],
            scan_patterns=self.settings.skill_scan_patterns,
            resource_dirs=self.settings.resource_dirs,
        )

    def _init_tools(self) -> None:
        """Initialize and register all tools."""
        self.registry = ToolRegistry()

        # Create tool instances
        tools = [
            SkillLoaderTool(skill_manager=self.skill_manager),
            SkillListerTool(
                skill_manager=self.skill_manager,
                skills_dir=self.settings.skills_dir,
            ),
            ResourceReaderTool(
                skill_manager=self.skill_manager,
                file_validator=self.file_validator,
            ),
            ScriptExecutorTool(
                skill_manager=self.skill_manager,
                file_validator=self.file_validator,
                workspace_dir=self.settings.workspace_dir,
                script_timeout=self.settings.script_timeout,
            ),
            FileReaderTool(
                workspace_dir=self.settings.workspace_dir,
                file_validator=self.file_validator,
            ),
            FileWriterTool(
                workspace_dir=self.settings.workspace_dir,
                file_validator=self.file_validator,
            ),
            FileEditorTool(
                workspace_dir=self.settings.workspace_dir,
                file_validator=self.file_validator,
            ),
        ]

        self.registry.register_many(tools)
        logger.info(f"Registered {self.registry.count()} tools")

    def _init_mcp_server(self) -> None:
        """Initialize the MCP server and handlers."""
        self.server = Server("skill-mcp-server")
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP protocol handlers."""

        @self.server.list_tools()
        async def list_tools():
            """Handle list_tools request."""
            return self.registry.list_tools()

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Handle tool invocation."""
            try:
                tool = self.registry.get_or_raise(name)
                result = tool.execute(**arguments)
            except ToolNotFoundError:
                result = f"Unknown tool: {name}"
            except Exception as e:
                logger.exception(f"Tool {name} failed")
                result = f"Error: {e}"

            return [TextContent(type="text", text=result)]

    async def run(self) -> None:
        """Run the MCP server.

        This starts the server and listens for MCP protocol
        messages on stdin/stdout.
        """
        logger.info("Starting Skill MCP Server...")

        # Pre-load skills
        skills = self.skill_manager.all()
        logger.info(f"Loaded {len(skills)} skills: {[s.name for s in skills]}")

        # Start the server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def create_server(
    skills_dir: Optional[Path] = None,
    workspace_dir: Optional[Path] = None,
    verbose: bool = False,
) -> SkillMCPServer:
    """Create a configured SkillMCPServer instance.

    This is the recommended way to create a server instance.

    Args:
        skills_dir: Path to skills directory.
        workspace_dir: Path to workspace directory.
        verbose: Enable verbose logging.

    Returns:
        Configured SkillMCPServer instance.

    Example:
        >>> server = create_server(
        ...     skills_dir=Path("./skills"),
        ...     workspace_dir=Path("./workspace"),
        ... )
        >>> import asyncio
        >>> asyncio.run(server.run())
    """
    # Setup logging
    setup_logging(verbose=verbose)

    # Load configuration
    settings = load_config(
        skills_dir=skills_dir,
        workspace_dir=workspace_dir,
        verbose=verbose,
    )

    return SkillMCPServer(settings)

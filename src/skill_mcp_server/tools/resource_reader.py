# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Resource reader tool - reads files from a skill's directory."""

from __future__ import annotations

from typing import Any

from ..skill.manager import SkillManager
from ..security.path_validator import PathValidator, PathValidationError
from ..security.file_validator import FileValidator, FileValidationError
from ..utils.logging import get_logger
from .base import BaseTool, ToolError

logger = get_logger("tools.resource_reader")


class ResourceReaderTool(BaseTool):
    """Tool for reading resource files from a skill's directory.

    This tool reads files like templates, examples, or reference
    documentation from within a skill's directory structure.
    """

    def __init__(
        self,
        skill_manager: SkillManager,
        file_validator: FileValidator,
    ) -> None:
        """Initialize the tool.

        Args:
            skill_manager: SkillManager instance.
            file_validator: FileValidator for checking file restrictions.
        """
        self.skill_manager = skill_manager
        self.file_validator = file_validator

    @property
    def name(self) -> str:
        return "skill_resource"

    @property
    def description(self) -> str:
        return (
            "Read a resource file from a skill's directory. "
            "Use this tool after loading a skill to read referenced files like templates, "
            "examples, or reference documentation. "
            "The resource_path should be relative to the skill's base directory "
            "(e.g., 'assets/template.md', 'references/api_reference.md')."
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill that owns the resource",
                },
                "resource_path": {
                    "type": "string",
                    "description": "Relative path to the resource file (e.g., 'assets/template.md')",
                },
            },
            "required": ["skill_name", "resource_path"],
        }

    def execute(
        self,
        skill_name: str = "",
        resource_path: str = "",
        **kwargs: Any,
    ) -> str:
        """Read a resource file from a skill.

        Args:
            skill_name: Name of the skill.
            resource_path: Relative path to the resource.

        Returns:
            Resource file content.
        """
        logger.info(f"Reading resource: {skill_name}/{resource_path}")

        # Validate inputs
        if not skill_name:
            raise ToolError("skill_name is required")
        if not resource_path:
            raise ToolError("resource_path is required")

        # Get the skill
        skill = self.skill_manager.get(skill_name)
        if not skill:
            available = ", ".join(self.skill_manager.names()) or "none"
            return f'Skill "{skill_name}" not found. Available skills: {available}'

        # Validate path is within skill directory
        base_dir = skill.base_dir
        path_validator = PathValidator(base_dir)

        try:
            target_path = path_validator.validate_file(resource_path)
        except PathValidationError as e:
            return f"Error: {e}"

        # Validate file type and size
        try:
            file_size = self.file_validator.validate_for_read(target_path)
        except FileValidationError as e:
            return f"Error: {e}"

        # Read the file
        try:
            content = target_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return f"Error: Cannot read file '{resource_path}' - not a valid text file"
        except Exception as e:
            return f"Error reading file: {e}"

        return self._format_output(resource_path, skill_name, file_size, content)

    def _format_output(
        self,
        resource_path: str,
        skill_name: str,
        file_size: int,
        content: str,
    ) -> str:
        """Format the output.

        Args:
            resource_path: Path to the resource.
            skill_name: Name of the skill.
            file_size: Size in bytes.
            content: File content.

        Returns:
            Formatted output.
        """
        return (
            f"## Resource: {resource_path}\n"
            f"**Skill**: {skill_name}\n"
            f"**Size**: {file_size} bytes\n\n"
            f"---\n\n{content}"
        )

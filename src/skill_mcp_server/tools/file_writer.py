# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""File writer tool - creates or overwrites files in the workspace."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..security.path_validator import PathValidator, PathValidationError
from ..security.file_validator import FileValidator, FileValidationError
from ..utils.logging import get_logger
from .base import BaseTool, ToolError

logger = get_logger("tools.file_writer")


class FileWriterTool(BaseTool):
    """Tool for creating or overwriting files in the workspace.

    This tool allows skills to generate output files in the
    workspace directory.
    """

    def __init__(
        self,
        workspace_dir: Path,
        file_validator: FileValidator,
    ) -> None:
        """Initialize the tool.

        Args:
            workspace_dir: Path to the workspace directory.
            file_validator: FileValidator for checking file restrictions.
        """
        self.workspace_dir = workspace_dir
        self.path_validator = PathValidator(workspace_dir)
        self.file_validator = file_validator

    @property
    def name(self) -> str:
        return "file_write"

    @property
    def description(self) -> str:
        return (
            "Create or overwrite a file in the workspace. "
            "Use this tool when a skill needs to generate output files."
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the workspace directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        }

    def execute(
        self,
        file_path: str = "",
        content: str = "",
        **kwargs: Any,
    ) -> str:
        """Write content to a file.

        Args:
            file_path: Relative path to the file.
            content: Content to write.

        Returns:
            Success message.
        """
        logger.info(f"Writing file: {file_path}")

        if not file_path:
            raise ToolError("file_path is required")

        # Validate path (allows non-existent files for creation)
        try:
            target_path = self.path_validator.validate(file_path)
        except PathValidationError as e:
            return f"Error: {e}"

        # Validate file type and content size
        try:
            content_size = self.file_validator.validate_for_write(target_path, content)
        except FileValidationError as e:
            return f"Error: {e}"

        # Create parent directories if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if file already exists
        is_new = not target_path.exists()
        action = "Created" if is_new else "Updated"

        # Write the file
        try:
            target_path.write_text(content, encoding="utf-8")
        except Exception as e:
            return f"Error writing file: {e}"

        return (
            f"## File {action}: {file_path}\n"
            f"**Workspace**: {self.workspace_dir}\n"
            f"**Size**: {content_size} bytes\n\n"
            f"File {action.lower()} successfully."
        )
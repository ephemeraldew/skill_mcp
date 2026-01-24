# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""File editor tool - edits existing files in the workspace."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..security.path_validator import PathValidator, PathValidationError
from ..security.file_validator import FileValidator, FileValidationError
from ..utils.logging import get_logger
from .base import BaseTool, ToolError

logger = get_logger("tools.file_editor")


class FileEditorTool(BaseTool):
    """Tool for editing existing files in the workspace.

    This tool uses search-and-replace to make targeted edits
    to files in the workspace directory.
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
        return "file_edit"

    @property
    def description(self) -> str:
        return (
            "Edit an existing file in the workspace using search and replace. "
            "The old_string must exist in the file and should be unique."
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
                "old_string": {
                    "type": "string",
                    "description": "Text to replace (must exist and be unique in the file)",
                },
                "new_string": {
                    "type": "string",
                    "description": "Replacement text",
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences instead of just the first",
                    "default": False,
                },
            },
            "required": ["file_path", "old_string", "new_string"],
        }

    def execute(
        self,
        file_path: str = "",
        old_string: str = "",
        new_string: str = "",
        replace_all: bool = False,
        **kwargs: Any,
    ) -> str:
        """Edit a file using search and replace.

        Args:
            file_path: Relative path to the file.
            old_string: Text to find and replace.
            new_string: Replacement text.
            replace_all: Whether to replace all occurrences.

        Returns:
            Success message.
        """
        logger.info(f"Editing file: {file_path}")

        # Validate inputs
        if not file_path:
            raise ToolError("file_path is required")
        if not old_string:
            raise ToolError("old_string is required")
        if old_string == new_string:
            return "Error: old_string and new_string must be different"

        # Validate path
        try:
            target_path = self.path_validator.validate_file(file_path)
        except PathValidationError as e:
            return f"Error: {e}"

        # Validate file type
        try:
            self.file_validator.validate_extension(target_path)
        except FileValidationError as e:
            return f"Error: {e}"

        # Read current content
        try:
            content = target_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return f"Error: Cannot read file '{file_path}' - not a valid text file"
        except Exception as e:
            return f"Error reading file: {e}"

        # Check if old_string exists
        if old_string not in content:
            return f"Error: old_string not found in file '{file_path}'"

        # Check for uniqueness if not replacing all
        match_count = content.count(old_string)
        if match_count > 1 and not replace_all:
            return (
                f"Error: Found {match_count} occurrences of old_string. "
                "Provide more context to make it unique, or set replace_all=true."
            )

        # Perform replacement
        if replace_all:
            new_content = content.replace(old_string, new_string)
            replaced_count = match_count
        else:
            new_content = content.replace(old_string, new_string, 1)
            replaced_count = 1

        # Validate new content size
        try:
            content_size = self.file_validator.validate_write_size(new_content)
        except FileValidationError as e:
            return f"Error: {e}"

        # Write the file
        try:
            target_path.write_text(new_content, encoding="utf-8")
        except Exception as e:
            return f"Error writing file: {e}"

        return (
            f"## File Edited: {file_path}\n"
            f"**Workspace**: {self.workspace_dir}\n"
            f"**Replacements**: {replaced_count}\n"
            f"**New Size**: {content_size} bytes\n\n"
            f"File edited successfully."
        )
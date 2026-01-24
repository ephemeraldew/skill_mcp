# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Path validation and security checks."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


class PathValidationError(Exception):
    """Raised when path validation fails."""

    pass


class PathValidator:
    """Validates file paths to prevent directory traversal attacks.

    This class ensures that file operations stay within designated
    safe directories (skills_dir, workspace_dir).
    """

    def __init__(self, base_dir: Path) -> None:
        """Initialize the path validator.

        Args:
            base_dir: The base directory that paths must stay within.
        """
        self.base_dir = base_dir.resolve()

    def validate(self, relative_path: str) -> Path:
        """Validate a relative path and return the resolved absolute path.

        Args:
            relative_path: Path relative to the base directory.

        Returns:
            Resolved absolute path.

        Raises:
            PathValidationError: If the path is outside the base directory.
        """
        # Construct the target path
        target_path = (self.base_dir / relative_path).resolve()

        # Check if the target is within the base directory
        if not self.is_within_base(target_path):
            raise PathValidationError(
                f"Security error: Path '{relative_path}' resolves outside "
                f"the allowed directory '{self.base_dir}'"
            )

        return target_path

    def is_within_base(self, path: Path) -> bool:
        """Check if a path is within the base directory.

        Args:
            path: Path to check (should be resolved/absolute).

        Returns:
            True if path is within base_dir, False otherwise.
        """
        try:
            path.resolve().relative_to(self.base_dir)
            return True
        except ValueError:
            return False

    def validate_exists(self, relative_path: str) -> Path:
        """Validate a path and ensure it exists.

        Args:
            relative_path: Path relative to the base directory.

        Returns:
            Resolved absolute path.

        Raises:
            PathValidationError: If path is invalid or doesn't exist.
        """
        target_path = self.validate(relative_path)

        if not target_path.exists():
            raise PathValidationError(f"Path not found: {relative_path}")

        return target_path

    def validate_file(self, relative_path: str) -> Path:
        """Validate a path and ensure it's an existing file.

        Args:
            relative_path: Path relative to the base directory.

        Returns:
            Resolved absolute path to the file.

        Raises:
            PathValidationError: If path is invalid, doesn't exist, or is not a file.
        """
        target_path = self.validate_exists(relative_path)

        if not target_path.is_file():
            raise PathValidationError(f"Not a file: {relative_path}")

        return target_path

    def validate_directory(self, relative_path: str) -> Path:
        """Validate a path and ensure it's an existing directory.

        Args:
            relative_path: Path relative to the base directory.

        Returns:
            Resolved absolute path to the directory.

        Raises:
            PathValidationError: If path is invalid, doesn't exist, or is not a directory.
        """
        target_path = self.validate_exists(relative_path)

        if not target_path.is_dir():
            raise PathValidationError(f"Not a directory: {relative_path}")

        return target_path

    def validate_parent_exists(self, relative_path: str) -> Path:
        """Validate a path for file creation (parent must exist or be creatable).

        Args:
            relative_path: Path relative to the base directory.

        Returns:
            Resolved absolute path.

        Raises:
            PathValidationError: If path is outside base directory.
        """
        return self.validate(relative_path)


def create_validator(base_dir: Path) -> PathValidator:
    """Factory function to create a PathValidator.

    Args:
        base_dir: The base directory for validation.

    Returns:
        Configured PathValidator instance.
    """
    return PathValidator(base_dir)
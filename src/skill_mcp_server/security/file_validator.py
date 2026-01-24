# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""File validation for type and size restrictions."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..config.defaults import (
    ALLOWED_FILE_EXTENSIONS,
    ALLOWED_SCRIPT_EXTENSIONS,
    MAX_FILE_SIZE,
    MAX_READ_SIZE,
)


class FileValidationError(Exception):
    """Raised when file validation fails."""

    pass


class FileValidator:
    """Validates files for type and size restrictions.

    This class ensures files meet the configured restrictions
    for extensions and sizes.
    """

    def __init__(
        self,
        allowed_extensions: frozenset[str] = ALLOWED_FILE_EXTENSIONS,
        allowed_script_extensions: frozenset[str] = ALLOWED_SCRIPT_EXTENSIONS,
        max_file_size: int = MAX_FILE_SIZE,
        max_read_size: int = MAX_READ_SIZE,
    ) -> None:
        """Initialize the file validator.

        Args:
            allowed_extensions: Set of allowed file extensions.
            allowed_script_extensions: Set of allowed script extensions.
            max_file_size: Maximum size for writing files (bytes).
            max_read_size: Maximum size for reading files (bytes).
        """
        self.allowed_extensions = allowed_extensions
        self.allowed_script_extensions = allowed_script_extensions
        self.max_file_size = max_file_size
        self.max_read_size = max_read_size

    def validate_extension(self, path: Path) -> None:
        """Validate that the file has an allowed extension.

        Args:
            path: Path to validate.

        Raises:
            FileValidationError: If the extension is not allowed.
        """
        suffix = path.suffix.lower()
        if suffix not in self.allowed_extensions:
            raise FileValidationError(
                f"File type '{suffix}' is not allowed. "
                f"Allowed types: {', '.join(sorted(self.allowed_extensions))}"
            )

    def validate_script_extension(self, path: Path) -> None:
        """Validate that the file has an allowed script extension.

        Args:
            path: Path to validate.

        Raises:
            FileValidationError: If the script extension is not allowed.
        """
        suffix = path.suffix.lower()
        if suffix not in self.allowed_script_extensions:
            raise FileValidationError(
                f"Script type '{suffix}' is not allowed. "
                f"Allowed types: {', '.join(sorted(self.allowed_script_extensions))}"
            )

    def validate_read_size(self, path: Path) -> int:
        """Validate that a file is not too large to read.

        Args:
            path: Path to the file.

        Returns:
            File size in bytes.

        Raises:
            FileValidationError: If the file is too large.
        """
        if not path.exists():
            raise FileValidationError(f"File not found: {path}")

        file_size = path.stat().st_size
        if file_size > self.max_read_size:
            raise FileValidationError(
                f"File too large to read: {file_size} bytes "
                f"(max: {self.max_read_size} bytes)"
            )
        return file_size

    def validate_write_size(self, content: str | bytes) -> int:
        """Validate that content is not too large to write.

        Args:
            content: Content to write.

        Returns:
            Content size in bytes.

        Raises:
            FileValidationError: If the content is too large.
        """
        if isinstance(content, str):
            content_size = len(content.encode("utf-8"))
        else:
            content_size = len(content)

        if content_size > self.max_file_size:
            raise FileValidationError(
                f"Content too large to write: {content_size} bytes "
                f"(max: {self.max_file_size} bytes)"
            )
        return content_size

    def validate_for_read(self, path: Path) -> int:
        """Perform all validations for reading a file.

        Args:
            path: Path to the file.

        Returns:
            File size in bytes.

        Raises:
            FileValidationError: If any validation fails.
        """
        self.validate_extension(path)
        return self.validate_read_size(path)

    def validate_for_write(self, path: Path, content: str | bytes) -> int:
        """Perform all validations for writing a file.

        Args:
            path: Target path.
            content: Content to write.

        Returns:
            Content size in bytes.

        Raises:
            FileValidationError: If any validation fails.
        """
        self.validate_extension(path)
        return self.validate_write_size(content)

    def validate_for_script(self, path: Path) -> None:
        """Validate that a file can be executed as a script.

        Args:
            path: Path to the script.

        Raises:
            FileValidationError: If the script extension is not allowed.
        """
        self.validate_script_extension(path)


def create_file_validator(
    allowed_extensions: Optional[frozenset[str]] = None,
    allowed_script_extensions: Optional[frozenset[str]] = None,
    max_file_size: Optional[int] = None,
    max_read_size: Optional[int] = None,
) -> FileValidator:
    """Factory function to create a FileValidator with custom settings.

    Args:
        allowed_extensions: Optional custom allowed extensions.
        allowed_script_extensions: Optional custom script extensions.
        max_file_size: Optional custom max write size.
        max_read_size: Optional custom max read size.

    Returns:
        Configured FileValidator instance.
    """
    kwargs = {}
    if allowed_extensions is not None:
        kwargs["allowed_extensions"] = allowed_extensions
    if allowed_script_extensions is not None:
        kwargs["allowed_script_extensions"] = allowed_script_extensions
    if max_file_size is not None:
        kwargs["max_file_size"] = max_file_size
    if max_read_size is not None:
        kwargs["max_read_size"] = max_read_size

    return FileValidator(**kwargs)
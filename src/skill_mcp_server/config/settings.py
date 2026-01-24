# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Settings data class for Skill MCP Server."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .defaults import (
    DEFAULT_SKILLS_DIR,
    DEFAULT_WORKSPACE_DIR,
    ALLOWED_FILE_EXTENSIONS,
    ALLOWED_SCRIPT_EXTENSIONS,
    MAX_FILE_SIZE,
    MAX_READ_SIZE,
    SCRIPT_TIMEOUT,
    RESOURCE_DIRS,
    SKILL_FILENAME,
    SKILL_SCAN_PATTERNS,
)


@dataclass
class Settings:
    """Configuration settings for Skill MCP Server.

    Attributes:
        skills_dir: Directory containing skill folders.
        workspace_dir: Working directory for file operations.
        allowed_file_extensions: File extensions allowed for read/write.
        allowed_script_extensions: Script extensions allowed for execution.
        max_file_size: Maximum file size for writing (bytes).
        max_read_size: Maximum file size for reading (bytes).
        script_timeout: Script execution timeout (seconds).
        resource_dirs: Subdirectories to scan for resources within skills.
        skill_filename: Expected filename for skill definitions.
        skill_scan_patterns: Glob patterns for discovering skills.
        verbose: Enable verbose logging.
    """

    # Directory settings
    skills_dir: Path = field(default_factory=lambda: Path.cwd() / DEFAULT_SKILLS_DIR)
    workspace_dir: Path = field(default_factory=lambda: Path.cwd() / DEFAULT_WORKSPACE_DIR)

    # File restrictions
    allowed_file_extensions: frozenset[str] = ALLOWED_FILE_EXTENSIONS
    allowed_script_extensions: frozenset[str] = ALLOWED_SCRIPT_EXTENSIONS

    # Size limits
    max_file_size: int = MAX_FILE_SIZE
    max_read_size: int = MAX_READ_SIZE

    # Execution limits
    script_timeout: int = SCRIPT_TIMEOUT

    # Skill discovery
    resource_dirs: tuple[str, ...] = RESOURCE_DIRS
    skill_filename: str = SKILL_FILENAME
    skill_scan_patterns: tuple[str, ...] = SKILL_SCAN_PATTERNS

    # Logging
    verbose: bool = False

    def __post_init__(self) -> None:
        """Ensure paths are Path objects and resolved."""
        if isinstance(self.skills_dir, str):
            self.skills_dir = Path(self.skills_dir)
        if isinstance(self.workspace_dir, str):
            self.workspace_dir = Path(self.workspace_dir)

        # Resolve to absolute paths
        self.skills_dir = self.skills_dir.resolve()
        self.workspace_dir = self.workspace_dir.resolve()

    def ensure_directories(self) -> None:
        """Create skills and workspace directories if they don't exist."""
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_args(
        cls,
        skills_dir: Optional[Path] = None,
        workspace_dir: Optional[Path] = None,
        verbose: bool = False,
    ) -> Settings:
        """Create Settings from command-line arguments.

        Args:
            skills_dir: Optional skills directory path.
            workspace_dir: Optional workspace directory path.
            verbose: Enable verbose logging.

        Returns:
            Configured Settings instance.
        """
        kwargs: dict = {"verbose": verbose}

        if skills_dir is not None:
            kwargs["skills_dir"] = skills_dir
        if workspace_dir is not None:
            kwargs["workspace_dir"] = workspace_dir

        return cls(**kwargs)
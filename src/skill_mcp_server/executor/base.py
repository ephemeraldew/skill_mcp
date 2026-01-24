# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Base executor interface for script execution."""

from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..config.defaults import SCRIPT_TIMEOUT


class ExecutionError(Exception):
    """Raised when script execution fails."""

    pass


@dataclass
class ExecutionResult:
    """Result of script execution.

    Attributes:
        exit_code: Process exit code (0 = success).
        stdout: Standard output content.
        stderr: Standard error content.
        timed_out: Whether the execution timed out.
    """

    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def success(self) -> bool:
        """Check if execution was successful.

        Returns:
            True if exit_code is 0 and didn't time out.
        """
        return self.exit_code == 0 and not self.timed_out

    def format_output(self, script_name: str, working_dir: Path) -> str:
        """Format the execution result as a readable string.

        Args:
            script_name: Name of the executed script.
            working_dir: Working directory used.

        Returns:
            Formatted output string.
        """
        parts = [
            f"## Script Execution: {script_name}",
            f"**Working Directory**: {working_dir}",
            f"**Exit Code**: {self.exit_code}",
            "",
        ]

        if self.stdout:
            parts.extend([
                "### stdout",
                "```",
                self.stdout.strip(),
                "```",
                "",
            ])

        if self.stderr:
            parts.extend([
                "### stderr",
                "```",
                self.stderr.strip(),
                "```",
                "",
            ])

        if self.timed_out:
            parts.append("**Status**: Execution timed out")
        elif self.success:
            parts.append("**Status**: Executed successfully")
        else:
            parts.append(f"**Status**: Failed with exit code {self.exit_code}")

        return "\n".join(parts)


class BaseExecutor(ABC):
    """Abstract base class for script executors.

    Each executor handles a specific type of script (Python, Shell, etc.).
    """

    # File extensions this executor handles
    extensions: tuple[str, ...] = ()

    def __init__(self, timeout: int = SCRIPT_TIMEOUT) -> None:
        """Initialize the executor.

        Args:
            timeout: Execution timeout in seconds.
        """
        self.timeout = timeout

    @abstractmethod
    def build_command(self, script_path: Path, args: list[str]) -> list[str]:
        """Build the command to execute the script.

        Args:
            script_path: Path to the script file.
            args: Command-line arguments.

        Returns:
            Command as a list of strings.
        """
        pass

    def execute(
        self,
        script_path: Path,
        working_dir: Path,
        args: Optional[list[str]] = None,
    ) -> ExecutionResult:
        """Execute a script.

        Args:
            script_path: Path to the script file.
            working_dir: Working directory for execution.
            args: Optional command-line arguments.

        Returns:
            ExecutionResult with output and status.

        Raises:
            ExecutionError: If execution fails unexpectedly.
        """
        args = args or []
        cmd = self.build_command(script_path, args)

        try:
            result = subprocess.run(
                cmd,
                cwd=str(working_dir),
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            return ExecutionResult(
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                timed_out=False,
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                exit_code=-1,
                stdout="",
                stderr=f"Execution timed out after {self.timeout} seconds",
                timed_out=True,
            )

        except Exception as e:
            raise ExecutionError(f"Failed to execute script: {e}") from e

    def can_execute(self, path: Path) -> bool:
        """Check if this executor can handle the given file.

        Args:
            path: Path to check.

        Returns:
            True if this executor handles the file's extension.
        """
        return path.suffix.lower() in self.extensions
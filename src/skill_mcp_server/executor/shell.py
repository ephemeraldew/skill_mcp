# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Shell script executor."""

from __future__ import annotations

from pathlib import Path

from .base import BaseExecutor


class ShellExecutor(BaseExecutor):
    """Executor for shell scripts (.sh, .bash files)."""

    extensions = (".sh", ".bash")

    def __init__(self, shell: str = "bash", **kwargs) -> None:
        """Initialize the shell executor.

        Args:
            shell: Shell to use (default: bash).
            **kwargs: Additional arguments for BaseExecutor.
        """
        super().__init__(**kwargs)
        self.shell = shell

    def build_command(self, script_path: Path, args: list[str]) -> list[str]:
        """Build command to execute a shell script.

        Args:
            script_path: Path to the shell script.
            args: Command-line arguments.

        Returns:
            Command as a list of strings.
        """
        cmd = [self.shell, str(script_path)]
        if args:
            cmd.extend(args)
        return cmd

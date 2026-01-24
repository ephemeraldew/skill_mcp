# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Python script executor."""

from __future__ import annotations

import sys
from pathlib import Path

from .base import BaseExecutor


class PythonExecutor(BaseExecutor):
    """Executor for Python scripts (.py files)."""

    extensions = (".py",)

    def build_command(self, script_path: Path, args: list[str]) -> list[str]:
        """Build command to execute a Python script.

        Uses the same Python interpreter that's running this server.

        Args:
            script_path: Path to the Python script.
            args: Command-line arguments.

        Returns:
            Command as a list of strings.
        """
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        return cmd
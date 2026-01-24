# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Node.js and TypeScript script executors."""

from __future__ import annotations

from pathlib import Path

from .base import BaseExecutor


class NodeExecutor(BaseExecutor):
    """Executor for JavaScript files (.js)."""

    extensions = (".js",)

    def __init__(self, node_cmd: str = "node", **kwargs) -> None:
        """Initialize the Node executor.

        Args:
            node_cmd: Node.js command (default: node).
            **kwargs: Additional arguments for BaseExecutor.
        """
        super().__init__(**kwargs)
        self.node_cmd = node_cmd

    def build_command(self, script_path: Path, args: list[str]) -> list[str]:
        """Build command to execute a JavaScript file.

        Args:
            script_path: Path to the JavaScript file.
            args: Command-line arguments.

        Returns:
            Command as a list of strings.
        """
        cmd = [self.node_cmd, str(script_path)]
        if args:
            cmd.extend(args)
        return cmd


class TypeScriptExecutor(BaseExecutor):
    """Executor for TypeScript files (.ts)."""

    extensions = (".ts",)

    def __init__(self, use_npx: bool = True, **kwargs) -> None:
        """Initialize the TypeScript executor.

        Args:
            use_npx: Whether to use npx ts-node (default: True).
            **kwargs: Additional arguments for BaseExecutor.
        """
        super().__init__(**kwargs)
        self.use_npx = use_npx

    def build_command(self, script_path: Path, args: list[str]) -> list[str]:
        """Build command to execute a TypeScript file.

        Uses npx ts-node by default for compatibility.

        Args:
            script_path: Path to the TypeScript file.
            args: Command-line arguments.

        Returns:
            Command as a list of strings.
        """
        if self.use_npx:
            cmd = ["npx", "ts-node", str(script_path)]
        else:
            cmd = ["ts-node", str(script_path)]

        if args:
            cmd.extend(args)
        return cmd

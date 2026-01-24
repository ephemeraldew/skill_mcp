# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Script executor tool - executes scripts from a skill's directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..skill.manager import SkillManager
from ..security.path_validator import PathValidator, PathValidationError
from ..security.file_validator import FileValidator, FileValidationError
from ..executor.factory import get_executor
from ..executor.base import ExecutionError
from ..utils.logging import get_logger
from .base import BaseTool, ToolError

logger = get_logger("tools.script_executor")


class ScriptExecutorTool(BaseTool):
    """Tool for executing scripts from a skill's directory.

    This tool executes Python, Shell, JavaScript, or TypeScript
    scripts that are bundled with a skill.
    """

    def __init__(
        self,
        skill_manager: SkillManager,
        file_validator: FileValidator,
        workspace_dir: Path,
        script_timeout: int = 120,
    ) -> None:
        """Initialize the tool.

        Args:
            skill_manager: SkillManager instance.
            file_validator: FileValidator for checking file restrictions.
            workspace_dir: Working directory for script execution.
            script_timeout: Timeout in seconds.
        """
        self.skill_manager = skill_manager
        self.file_validator = file_validator
        self.workspace_dir = workspace_dir
        self.script_timeout = script_timeout

    @property
    def name(self) -> str:
        return "skill_script"

    @property
    def description(self) -> str:
        return (
            "Execute a script from a skill's scripts/ directory. "
            "Use this tool to run Python (.py), Shell (.sh/.bash), "
            "JavaScript (.js), or TypeScript (.ts) scripts bundled with a skill. "
            "Scripts are executed in the workspace directory."
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill that owns the script",
                },
                "script_path": {
                    "type": "string",
                    "description": "Relative path to the script (e.g., 'scripts/init.py')",
                },
                "args": {
                    "type": "string",
                    "description": "Command-line arguments to pass to the script",
                    "default": "",
                },
            },
            "required": ["skill_name", "script_path"],
        }

    def execute(
        self,
        skill_name: str = "",
        script_path: str = "",
        args: str = "",
        **kwargs: Any,
    ) -> str:
        """Execute a script from a skill.

        Args:
            skill_name: Name of the skill.
            script_path: Relative path to the script.
            args: Command-line arguments.

        Returns:
            Script execution output.
        """
        logger.info(f"Executing script: {skill_name}/{script_path} {args}")

        # Validate inputs
        if not skill_name:
            raise ToolError("skill_name is required")
        if not script_path:
            raise ToolError("script_path is required")

        # Get the skill
        skill = self.skill_manager.get(skill_name)
        if not skill:
            available = ", ".join(self.skill_manager.names()) or "none"
            return f'Skill "{skill_name}" not found. Available skills: {available}'

        # Validate path is within skill directory
        base_dir = skill.base_dir
        path_validator = PathValidator(base_dir)

        try:
            target_path = path_validator.validate_file(script_path)
        except PathValidationError as e:
            return f"Error: {e}"

        # Validate script extension
        try:
            self.file_validator.validate_for_script(target_path)
        except FileValidationError as e:
            return f"Error: {e}"

        # Get executor for this script type
        try:
            executor = get_executor(target_path, timeout=self.script_timeout)
        except ExecutionError as e:
            return f"Error: {e}"

        # Parse arguments
        arg_list = args.split() if args.strip() else []

        # Execute the script
        try:
            result = executor.execute(
                script_path=target_path,
                working_dir=self.workspace_dir,
                args=arg_list,
            )
        except ExecutionError as e:
            return f"Error executing script: {e}"

        return self._format_output(script_path, skill_name, result)

    def _format_output(self, script_path: str, skill_name: str, result) -> str:
        """Format the execution result.

        Args:
            script_path: Path to the script.
            skill_name: Name of the skill.
            result: ExecutionResult object.

        Returns:
            Formatted output.
        """
        parts = [
            f"## Script Execution: {script_path}",
            f"**Skill**: {skill_name}",
            f"**Working Directory**: {self.workspace_dir}",
            f"**Exit Code**: {result.exit_code}",
            "",
        ]

        if result.stdout:
            parts.extend([
                "### stdout",
                "```",
                result.stdout.strip(),
                "```",
                "",
            ])

        if result.stderr:
            parts.extend([
                "### stderr",
                "```",
                result.stderr.strip(),
                "```",
                "",
            ])

        if result.timed_out:
            parts.append(f"**Status**: Timed out after {self.script_timeout} seconds")
        elif result.success:
            parts.append("**Status**: Executed successfully")
        else:
            parts.append(f"**Status**: Failed with exit code {result.exit_code}")

        return "\n".join(parts)
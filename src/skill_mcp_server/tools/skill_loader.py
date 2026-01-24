# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Skill loader tool - loads a skill's content and metadata."""

from __future__ import annotations

from typing import Any

from ..skill.manager import SkillManager
from ..utils.logging import get_logger
from .base import BaseTool, ToolError

logger = get_logger("tools.skill_loader")


class SkillLoaderTool(BaseTool):
    """Tool for loading a skill's content.

    This tool loads a skill by name and returns its full content,
    including available scripts and resources.
    """

    def __init__(self, skill_manager: SkillManager) -> None:
        """Initialize the tool.

        Args:
            skill_manager: SkillManager instance for accessing skills.
        """
        self.skill_manager = skill_manager

    @property
    def name(self) -> str:
        return "skill"

    @property
    def description(self) -> str:
        """Generate description with available skills list."""
        skills = self.skill_manager.all()

        if not skills:
            return (
                "Load a skill to get detailed instructions for a specific task. "
                "No skills are currently available."
            )

        skill_list = "\n".join([
            f"  <skill>\n"
            f"    <name>{skill.name}</name>\n"
            f"    <description>{skill.description}</description>\n"
            f"  </skill>"
            for skill in skills
        ])

        return (
            "Load a skill to get detailed instructions for a specific task. "
            "Skills provide specialized knowledge and step-by-step guidance. "
            "Use this when a task matches an available skill's description.\n"
            f"<available_skills>\n{skill_list}\n</available_skills>"
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the skill to load",
                }
            },
            "required": ["name"],
        }

    def execute(self, name: str = "", **kwargs: Any) -> str:
        """Load a skill by name.

        Args:
            name: Skill name to load.

        Returns:
            Skill content with metadata.
        """
        logger.info(f"Loading skill: {name}")

        if not name:
            raise ToolError("Skill name is required")

        skill = self.skill_manager.get(name)

        if not skill:
            return self._format_not_found(name)

        return self._format_skill(skill)

    def _format_not_found(self, name: str) -> str:
        """Format error message when skill is not found.

        Args:
            name: Skill name that wasn't found.

        Returns:
            Formatted error message.
        """
        all_skills = self.skill_manager.all()

        if all_skills:
            skill_list = "\n".join([
                f"  - {s.name}: {s.description[:80]}..."
                if len(s.description) > 80
                else f"  - {s.name}: {s.description}"
                for s in all_skills
            ])
            return (
                f'Skill "{name}" not found.\n\n'
                f"Available skills ({len(all_skills)} total):\n{skill_list}"
            )

        return f'Skill "{name}" not found. No skills are currently available.'

    def _format_skill(self, skill) -> str:
        """Format a skill for output.

        Args:
            skill: SkillInfo object.

        Returns:
            Formatted skill content.
        """
        resources, scripts = self.skill_manager.list_skill_files(skill)

        output = [
            f"## Skill: {skill.name}",
            "",
            f"**Base directory**: {skill.base_dir}",
            f"**Category**: {skill.category or 'uncategorized'}",
            "",
        ]

        if scripts:
            output.append("**Available scripts** (use `skill_script` tool to execute):")
            for script in scripts:
                output.append(f"  - {script}")
            output.append("")

        if resources:
            output.append("**Available resources** (use `skill_resource` tool to read):")
            for resource in resources:
                output.append(f"  - {resource}")
            output.append("")

        output.append(skill.content.strip())

        return "\n".join(output)

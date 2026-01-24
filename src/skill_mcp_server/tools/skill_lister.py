# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Skill lister tool - lists all available skills."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..skill.manager import SkillManager
from ..utils.logging import get_logger
from .base import BaseTool

logger = get_logger("tools.skill_lister")


class SkillListerTool(BaseTool):
    """Tool for listing all available skills.

    This tool returns a list of all discovered skills,
    optionally grouped by category.
    """

    def __init__(
        self,
        skill_manager: SkillManager,
        skills_dir: Path,
    ) -> None:
        """Initialize the tool.

        Args:
            skill_manager: SkillManager instance.
            skills_dir: Path to the skills directory.
        """
        self.skill_manager = skill_manager
        self.skills_dir = skills_dir

    @property
    def name(self) -> str:
        return "list_skills"

    @property
    def description(self) -> str:
        return (
            "List all available skills with their names and descriptions. "
            "Use this to discover what skills are available before loading one."
        )

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    def execute(self, **kwargs: Any) -> str:
        """List all available skills.

        Returns:
            Formatted list of skills.
        """
        logger.info("Listing all skills")

        # Force reload to get latest skills
        self.skill_manager.reload()
        skills = self.skill_manager.all()

        if not skills:
            return self._format_no_skills()

        return self._format_skills_list(skills)

    def _format_no_skills(self) -> str:
        """Format message when no skills are available.

        Returns:
            Formatted message.
        """
        return (
            "No skills are currently available.\n"
            f"Please add skills to: {self.skills_dir}\n\n"
            "Each skill should be a directory containing a SKILL.md file."
        )

    def _format_skills_list(self, skills) -> str:
        """Format the skills list.

        Args:
            skills: List of SkillInfo objects.

        Returns:
            Formatted skills list.
        """
        output = [
            f"## Available Skills ({len(skills)} total)",
            "",
            f"**Skills directory**: {self.skills_dir}",
            "",
        ]

        # Group by category
        by_category = self.skill_manager.list_by_category()

        for category, category_skills in sorted(by_category.items()):
            output.append(f"### {category}")
            output.append("")

            for skill in category_skills:
                output.append(f"- **{skill.name}**: {skill.description}")

            output.append("")

        return "\n".join(output)

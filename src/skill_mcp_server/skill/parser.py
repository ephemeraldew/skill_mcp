# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""SKILL.md file parser."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..utils.frontmatter import parse_frontmatter
from ..utils.markdown import extract_description
from ..utils.logging import get_logger
from .models import SkillInfo, SkillMetadata

logger = get_logger("skill.parser")


class SkillParseError(Exception):
    """Raised when skill parsing fails."""

    pass


class SkillParser:
    """Parser for SKILL.md files.

    Handles both standard format (with YAML frontmatter) and
    simplified format (name from directory, description from content).
    """

    def __init__(self, skill_filename: str = "SKILL.md") -> None:
        """Initialize the parser.

        Args:
            skill_filename: Expected skill file name.
        """
        self.skill_filename = skill_filename

    def parse(
        self,
        path: Path,
        base_dir: Optional[Path] = None,
    ) -> SkillInfo:
        """Parse a SKILL.md file into a SkillInfo object.

        Args:
            path: Path to the SKILL.md file.
            base_dir: Base directory for inferring category.

        Returns:
            Parsed SkillInfo object.

        Raises:
            SkillParseError: If parsing fails.
        """
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            raise SkillParseError(f"Failed to read {path}: {e}") from e

        # Parse frontmatter
        frontmatter, markdown = parse_frontmatter(content)
        metadata = SkillMetadata.from_dict(frontmatter)

        # Determine skill name
        name = self._resolve_name(metadata, path)

        # Determine description
        description = self._resolve_description(metadata, markdown)

        # Determine category from directory structure
        category = self._resolve_category(path, base_dir)

        return SkillInfo(
            name=name,
            description=description,
            location=path,
            content=markdown if markdown else content,
            category=category,
        )

    def _resolve_name(self, metadata: SkillMetadata, path: Path) -> str:
        """Resolve the skill name.

        Priority:
        1. Frontmatter 'name' field
        2. Parent directory name (if file is SKILL.md)
        3. File stem

        Args:
            metadata: Parsed metadata.
            path: Path to the skill file.

        Returns:
            Resolved skill name.
        """
        if metadata.name:
            return metadata.name

        if path.name == self.skill_filename:
            return path.parent.name

        return path.stem

    def _resolve_description(
        self,
        metadata: SkillMetadata,
        markdown: str,
    ) -> str:
        """Resolve the skill description.

        Priority:
        1. Frontmatter 'description' field
        2. First paragraph of markdown content

        Args:
            metadata: Parsed metadata.
            markdown: Markdown content.

        Returns:
            Resolved description.
        """
        if metadata.description:
            return metadata.description

        return extract_description(markdown)

    def _resolve_category(
        self,
        path: Path,
        base_dir: Optional[Path],
    ) -> Optional[str]:
        """Resolve the skill category from directory structure.

        Args:
            path: Path to the skill file.
            base_dir: Base skills directory.

        Returns:
            Category string or None.
        """
        if base_dir is None:
            return None

        try:
            rel_path = path.relative_to(base_dir)
            # Get all parts except the filename and immediate parent (skill name)
            parts = rel_path.parts[:-2]  # Remove filename and skill directory
            if parts:
                return "/".join(parts)
        except ValueError:
            pass

        return None

    def can_parse(self, path: Path) -> bool:
        """Check if a path can be parsed as a skill.

        Args:
            path: Path to check.

        Returns:
            True if the file appears to be a valid skill file.
        """
        if not path.is_file():
            return False

        if path.name != self.skill_filename:
            return False

        # Check for hidden files or __pycache__
        path_str = str(path)
        if "__pycache__" in path_str or "/.git" in path_str:
            return False

        return True
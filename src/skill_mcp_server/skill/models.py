# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Data models for skills."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class SkillInfo:
    """Immutable data class representing a skill.

    Attributes:
        name: Unique identifier for the skill.
        description: Human-readable description of what the skill does.
        location: Path to the SKILL.md file.
        content: The markdown content (body without frontmatter).
        category: Optional category (inferred from directory structure).
        base_dir: The skill's root directory (parent of SKILL.md).
    """

    name: str
    description: str
    location: Path
    content: str
    category: Optional[str] = None

    @property
    def base_dir(self) -> Path:
        """Get the skill's base directory.

        Returns:
            Path to the directory containing SKILL.md.
        """
        return self.location.parent

    def has_scripts(self) -> bool:
        """Check if the skill has a scripts directory.

        Returns:
            True if scripts/ directory exists.
        """
        return (self.base_dir / "scripts").is_dir()

    def has_references(self) -> bool:
        """Check if the skill has a references directory.

        Returns:
            True if references/ directory exists.
        """
        return (self.base_dir / "references").is_dir()

    def has_assets(self) -> bool:
        """Check if the skill has an assets directory.

        Returns:
            True if assets/ directory exists.
        """
        return (self.base_dir / "assets").is_dir()

    def get_scripts_dir(self) -> Optional[Path]:
        """Get the scripts directory if it exists.

        Returns:
            Path to scripts/ or None.
        """
        scripts_dir = self.base_dir / "scripts"
        return scripts_dir if scripts_dir.is_dir() else None

    def get_references_dir(self) -> Optional[Path]:
        """Get the references directory if it exists.

        Returns:
            Path to references/ or None.
        """
        refs_dir = self.base_dir / "references"
        return refs_dir if refs_dir.is_dir() else None

    def get_assets_dir(self) -> Optional[Path]:
        """Get the assets directory if it exists.

        Returns:
            Path to assets/ or None.
        """
        assets_dir = self.base_dir / "assets"
        return assets_dir if assets_dir.is_dir() else None


@dataclass
class SkillMetadata:
    """Metadata extracted from SKILL.md frontmatter.

    Attributes:
        name: Skill name (optional, can be inferred from directory).
        description: Skill description (optional, can be inferred from content).
        license: License information.
        version: Skill version.
        author: Skill author.
        tags: List of tags/keywords.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    license: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> SkillMetadata:
        """Create SkillMetadata from a dictionary (parsed frontmatter).

        Args:
            data: Dictionary of frontmatter data.

        Returns:
            SkillMetadata instance.
        """
        tags = data.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        return cls(
            name=data.get("name"),
            description=data.get("description"),
            license=data.get("license"),
            version=data.get("version"),
            author=data.get("author"),
            tags=tags,
        )

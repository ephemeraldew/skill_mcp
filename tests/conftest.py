# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Pytest configuration and fixtures."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def skills_dir(temp_dir: Path) -> Path:
    """Create a skills directory with a sample skill."""
    skills = temp_dir / "skills"
    skills.mkdir()

    # Create a sample skill
    sample_skill = skills / "sample-skill"
    sample_skill.mkdir()

    skill_md = sample_skill / "SKILL.md"
    skill_md.write_text("""---
name: sample-skill
description: A sample skill for testing
---

# Sample Skill

This is a sample skill for testing purposes.

## Usage

Use this skill to test the MCP server.
""")

    # Create scripts directory
    scripts = sample_skill / "scripts"
    scripts.mkdir()
    (scripts / "hello.py").write_text("""#!/usr/bin/env python3
print("Hello from sample-skill!")
""")

    # Create references directory
    refs = sample_skill / "references"
    refs.mkdir()
    (refs / "doc.md").write_text("# Reference Doc\n\nSome documentation.")

    # Create assets directory
    assets = sample_skill / "assets"
    assets.mkdir()
    (assets / "template.txt").write_text("Template content")

    return skills


@pytest.fixture
def workspace_dir(temp_dir: Path) -> Path:
    """Create a workspace directory."""
    workspace = temp_dir / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def sample_skill_content() -> str:
    """Return sample SKILL.md content."""
    return """---
name: test-skill
description: Test skill for unit tests
---

# Test Skill

Test content here.
"""
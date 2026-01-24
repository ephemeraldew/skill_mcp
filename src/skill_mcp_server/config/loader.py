# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Configuration loader for Skill MCP Server."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from .settings import Settings


def load_config(
    skills_dir: Optional[Path] = None,
    workspace_dir: Optional[Path] = None,
    verbose: bool = False,
) -> Settings:
    """Load configuration with environment variable overrides.

    Priority (highest to lowest):
    1. Function arguments
    2. Environment variables
    3. Default values

    Environment variables:
    - SKILL_MCP_SKILLS_DIR: Skills directory path
    - SKILL_MCP_WORKSPACE_DIR: Workspace directory path
    - SKILL_MCP_VERBOSE: Enable verbose logging ("1", "true", "yes")

    Args:
        skills_dir: Optional skills directory (overrides env var).
        workspace_dir: Optional workspace directory (overrides env var).
        verbose: Enable verbose logging (overrides env var).

    Returns:
        Configured Settings instance.
    """
    # Check environment variables for defaults
    env_skills_dir = os.environ.get("SKILL_MCP_SKILLS_DIR")
    env_workspace_dir = os.environ.get("SKILL_MCP_WORKSPACE_DIR")
    env_verbose = os.environ.get("SKILL_MCP_VERBOSE", "").lower() in ("1", "true", "yes")

    # Apply priority: argument > env var > default
    final_skills_dir = skills_dir
    if final_skills_dir is None and env_skills_dir:
        final_skills_dir = Path(env_skills_dir)

    final_workspace_dir = workspace_dir
    if final_workspace_dir is None and env_workspace_dir:
        final_workspace_dir = Path(env_workspace_dir)

    final_verbose = verbose or env_verbose

    return Settings.from_args(
        skills_dir=final_skills_dir,
        workspace_dir=final_workspace_dir,
        verbose=final_verbose,
    )

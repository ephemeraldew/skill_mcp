# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""YAML frontmatter parsing utilities.

This module provides a simple YAML frontmatter parser that doesn't
require external dependencies like PyYAML.
"""

from __future__ import annotations

import re
from typing import Any


# Pattern to match YAML frontmatter delimited by ---
FRONTMATTER_PATTERN = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n(.*)$",
    re.DOTALL
)


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content.

    This is a simple implementation that handles basic key: value pairs
    without requiring external YAML libraries.

    Supported formats:
    - Simple key: value pairs
    - Quoted values (single or double quotes)
    - Comments (lines starting with #)

    Args:
        content: Full markdown content with optional frontmatter.

    Returns:
        Tuple of (frontmatter dict, remaining markdown content).
        If no frontmatter is found, returns ({}, original content).

    Example:
        >>> content = '''---
        ... name: my-skill
        ... description: "A great skill"
        ... ---
        ... # My Skill
        ... Content here...
        ... '''
        >>> meta, body = parse_frontmatter(content)
        >>> meta['name']
        'my-skill'
    """
    match = FRONTMATTER_PATTERN.match(content)

    if not match:
        return {}, content

    yaml_content = match.group(1)
    markdown_content = match.group(2)

    frontmatter = _parse_yaml_simple(yaml_content)

    return frontmatter, markdown_content


def _parse_yaml_simple(yaml_content: str) -> dict[str, Any]:
    """Parse simple YAML key-value pairs.

    Args:
        yaml_content: YAML content string.

    Returns:
        Dictionary of parsed key-value pairs.
    """
    result: dict[str, Any] = {}

    for line in yaml_content.split("\n"):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Parse key: value
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Remove quotes if present
            value = _unquote(value)

            result[key] = value

    return result


def _unquote(value: str) -> str:
    """Remove surrounding quotes from a string.

    Args:
        value: String that may be quoted.

    Returns:
        String with quotes removed.
    """
    if len(value) >= 2:
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
    return value


def has_frontmatter(content: str) -> bool:
    """Check if content has YAML frontmatter.

    Args:
        content: Markdown content to check.

    Returns:
        True if frontmatter is present, False otherwise.
    """
    return FRONTMATTER_PATTERN.match(content) is not None

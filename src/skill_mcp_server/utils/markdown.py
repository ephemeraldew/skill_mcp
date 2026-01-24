# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Markdown processing utilities."""

from __future__ import annotations


def extract_description(content: str, max_length: int = 100) -> str:
    """Extract a description from markdown content.

    Attempts to find the first meaningful paragraph that isn't
    a heading or separator.

    Args:
        content: Markdown content.
        max_length: Maximum description length.

    Returns:
        Extracted description, or default message if none found.
    """
    lines = content.strip().split("\n")

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip headings
        if line.startswith("#"):
            continue

        # Skip horizontal rules
        if line.startswith("---") or line.startswith("==="):
            continue

        # Skip list markers at the start (but keep the content)
        if line.startswith(("- ", "* ", "+ ")):
            line = line[2:].strip()
        elif len(line) > 2 and line[0].isdigit() and line[1] in (".", ")"):
            line = line[2:].strip()

        # Found a content line
        if line:
            return _truncate(line, max_length)

    return "No description available"


def _truncate(text: str, max_length: int) -> str:
    """Truncate text to maximum length with ellipsis.

    Args:
        text: Text to truncate.
        max_length: Maximum length.

    Returns:
        Truncated text with ellipsis if needed.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def extract_title(content: str) -> str | None:
    """Extract the first heading from markdown content.

    Args:
        content: Markdown content.

    Returns:
        Title text without # prefix, or None if no heading found.
    """
    lines = content.strip().split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            # Remove # characters and whitespace
            return line.lstrip("#").strip()

    return None


def count_lines(content: str) -> int:
    """Count the number of lines in content.

    Args:
        content: Text content.

    Returns:
        Number of lines.
    """
    return len(content.splitlines())

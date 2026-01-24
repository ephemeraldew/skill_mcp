# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Default configuration values for Skill MCP Server."""

# Directory defaults
DEFAULT_SKILLS_DIR = "skills"
DEFAULT_WORKSPACE_DIR = "workspace"

# File type restrictions
ALLOWED_FILE_EXTENSIONS: frozenset[str] = frozenset({
    ".md", ".txt", ".json", ".yaml", ".yml",
    ".py", ".sh", ".bash", ".js", ".ts",
    ".html", ".css", ".xml", ".csv", ".log",
    ".toml", ".ini", ".cfg", ".conf",
})

# Script type restrictions
ALLOWED_SCRIPT_EXTENSIONS: frozenset[str] = frozenset({
    ".py",    # Python
    ".sh",    # Shell
    ".bash",  # Bash
    ".js",    # JavaScript
    ".ts",    # TypeScript
})

# Size limits (in bytes)
MAX_FILE_SIZE = 100 * 1024      # 100KB for writing
MAX_READ_SIZE = 1024 * 1024     # 1MB for reading

# Execution limits
SCRIPT_TIMEOUT = 120  # seconds

# Resource directories within a skill
RESOURCE_DIRS: tuple[str, ...] = (
    "assets",
    "references",
    "examples",
    "templates",
)

# Skill file name
SKILL_FILENAME = "SKILL.md"

# Scan patterns for skill discovery
SKILL_SCAN_PATTERNS: tuple[str, ...] = (
    "*/SKILL.md",  # Standard: skills/skill-name/SKILL.md
)
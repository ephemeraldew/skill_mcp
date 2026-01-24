# Example Skills

This directory contains example skills to help you get started with Skill MCP Server.

## Available Examples

### skill-creator

A meta-skill that helps you create new skills. Use this skill when you want to:

- Create a new skill from scratch
- Understand the skill format and structure
- Package skills for distribution

**Usage:**

1. Copy the `skill-creator` folder to your skills directory
2. Start the MCP server
3. Ask your AI agent to "create a new skill for [your use case]"

## Using Examples

To use these examples:

```bash
# Copy an example to your skills directory
cp -r examples/skill-creator /path/to/your/skills/

# Or copy all examples
cp -r examples/* /path/to/your/skills/
```

## Creating Your Own Skills

Each skill is a folder containing:

```
my-skill/
├── SKILL.md              # Required: Main skill file
├── scripts/              # Optional: Executable scripts
│   └── helper.py
├── references/           # Optional: Reference documentation
│   └── api_docs.md
└── assets/               # Optional: Templates, images, etc.
    └── template.md
```

### SKILL.md Format

```markdown
---
name: my-skill
description: What this skill does and when to use it
---

# My Skill

Instructions for the AI agent...
```

See the `skill-creator` example for detailed guidance on creating effective skills.

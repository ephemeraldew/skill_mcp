# Getting Started

This guide will help you get up and running with Skill MCP Server in just a few minutes.

## Prerequisites

- Python 3.10 or higher
- An MCP-compatible AI client (e.g., Claude Desktop, Claude Code)

## Installation

### Using pip

```bash
pip install skill-mcp-server
```

### Using uv (recommended)

```bash
uv pip install skill-mcp-server
```

### From source

```bash
git clone https://github.com/your-org/skill-mcp-server.git
cd skill-mcp-server
pip install -e .
```

## Basic Usage

### 1. Create a Skills Directory

```bash
mkdir skills
```

### 2. Add Your First Skill

Create a simple skill:

```bash
mkdir skills/hello-world
```

Create `skills/hello-world/SKILL.md`:

```markdown
---
name: hello-world
description: A simple greeting skill that demonstrates the basics
---

# Hello World Skill

This is a simple skill that demonstrates the basic structure.

## Usage

When the user asks for a greeting, respond with a friendly message.

## Example

User: "Say hello"
Response: "Hello! I'm using the hello-world skill!"
```

### 3. Start the Server

```bash
skill-mcp-server --skills-dir ./skills
```

### 4. Configure Your AI Client

#### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the equivalent config file:

```json
{
  "mcpServers": {
    "skill-server": {
      "command": "skill-mcp-server",
      "args": ["--skills-dir", "/path/to/your/skills"]
    }
  }
}
```

#### Claude Code

Edit `~/.claude.json`:

```json
{
  "mcpServers": {
    "skill-server": {
      "command": "skill-mcp-server",
      "args": [
        "--skills-dir", "/path/to/your/skills",
        "--workspace", "/path/to/workspace"
      ]
    }
  }
}
```

## Next Steps

- [Creating Skills](creating-skills.md) - Learn how to create powerful skills
- [Skill Format Reference](skill-format.md) - Detailed documentation of the skill format
- Check out the [examples](../examples/) for inspiration
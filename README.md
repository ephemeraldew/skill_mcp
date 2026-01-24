# Skill MCP Server

<p align="center">
  <strong>Turn any AI agent into a specialist — just drop in a skill folder.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#creating-skills">Creating Skills</a> •
  <a href="#documentation">Documentation</a>
</p>

---

**Skill MCP Server** is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that enables AI agents like Claude to dynamically load and use modular "skills".

Think of it as a **plugin system for AI agents** — drop a skill folder into the directory, and your agent instantly gains new capabilities. No coding required, no server restarts needed.

## Why Skill MCP Server?

| Traditional Approach | With Skill MCP Server |
|---------------------|----------------------|
| Write code to extend agent capabilities | Just copy a folder |
| Restart services to apply changes | Hot reload, instant availability |
| Each capability developed separately | Community-shared, plug-and-play |
| Complex integration work | Zero configuration |

## Features

- **Instant Capability Extension** — Drop skill folders, gain superpowers
- **Zero Configuration** — Skills are auto-discovered and loaded
- **Hot Reload** — Add new skills without restarting the server
- **Multi-Language Scripts** — Execute Python, Shell, JavaScript, TypeScript
- **Secure by Design** — Path validation, sandboxed file operations
- **Resource Bundling** — Include templates, references, and assets with skills

## Quick Start

### Installation

```bash
# Using pip
pip install skill-mcp-server

# Using uv (recommended)
uv pip install skill-mcp-server
```

### 30-Second Setup

```bash
# 1. Create a skills directory
mkdir skills

# 2. Download or create a skill (example: copy the skill-creator)
cp -r examples/skill-creator skills/

# 3. Start the server
skill-mcp-server --skills-dir ./skills
```

That's it! Your AI agent can now use the skill.

### Configure with Claude Desktop

Add to your `claude_desktop_config.json`:

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

### Configure with Claude Code

Add to your `~/.claude.json`:

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

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Agent (Claude)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ MCP Protocol
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Skill MCP Server                            │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │   skill   │  │  skill_   │  │  skill_   │  │   file_   │    │
│  │  loader   │  │ resource  │  │  script   │  │   ops     │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Skills Directory                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ data-analyst│  │ doc-writer  │  │ api-helper  │  ...        │
│  │  SKILL.md   │  │  SKILL.md   │  │  SKILL.md   │             │
│  │  scripts/   │  │  templates/ │  │  references/│             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `skill` | Load a skill to get detailed instructions |
| `list_skills` | List all available skills |
| `skill_resource` | Read resource files from a skill |
| `skill_script` | Execute scripts bundled with a skill |
| `file_read` | Read files from workspace |
| `file_write` | Write files to workspace |
| `file_edit` | Edit existing files in workspace |

## Creating Skills

A skill is simply a folder containing a `SKILL.md` file:

```
my-skill/
├── SKILL.md              # Required: Instructions for the AI
├── scripts/              # Optional: Executable scripts
│   └── process_data.py
├── references/           # Optional: Reference documentation
│   └── api_docs.md
└── assets/               # Optional: Templates, images, etc.
    └── report_template.md
```

### SKILL.md Format

```markdown
---
name: my-skill
description: Brief description of what this skill does and when to use it
---

# My Skill

## Overview

Explain what this skill enables the AI to do.

## Usage

Step-by-step instructions for the AI agent...

## Available Resources

- `scripts/process_data.py` - Process input data
- `assets/report_template.md` - Output template
```

### Example: Data Analyst Skill

```markdown
---
name: data-analyst
description: Analyze CSV data and generate insights reports
---

# Data Analyst

## When to Use

Use this skill when the user wants to:
- Analyze CSV or tabular data
- Generate statistical summaries
- Create data visualizations

## Workflow

1. Read the data file using `file_read`
2. Execute `scripts/analyze.py` for statistical analysis
3. Use `assets/report_template.md` to format the output
4. Write the report using `file_write`
```

## Use Cases

- **Data Analysis** — Agent becomes a data scientist
- **Document Generation** — Agent creates professional documents
- **API Integration** — Agent works with specific APIs
- **Code Review** — Agent follows your team's standards
- **DevOps Tasks** — Agent automates deployment workflows

## Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Creating Skills](docs/creating-skills.md)
- [Skill Format Reference](docs/skill-format.md)
- [API Reference](docs/api/)

## Development

```bash
# Clone the repository
git clone https://github.com/your-org/skill-mcp-server.git
cd skill-mcp-server

# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with the <a href="https://modelcontextprotocol.io/">Model Context Protocol</a></sub>
</p>
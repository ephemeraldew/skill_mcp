# Creating Skills

This guide covers everything you need to know about creating effective skills for Skill MCP Server.

## What is a Skill?

A skill is a self-contained package that extends an AI agent's capabilities. It consists of:

- **SKILL.md** - Instructions for the AI (required)
- **scripts/** - Executable code (optional)
- **references/** - Documentation to load on-demand (optional)
- **assets/** - Templates and resources (optional)

## Skill Structure

```
my-skill/
├── SKILL.md              # Required: Main instructions
├── scripts/              # Optional: Executable scripts
│   ├── process.py
│   └── validate.sh
├── references/           # Optional: Reference documentation
│   └── api_docs.md
└── assets/               # Optional: Templates, images, etc.
    └── template.md
```

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: my-skill
description: Brief description of what this skill does and when to use it
---
```

**Best practices for description:**
- Be specific about what the skill does
- Include when the skill should be used
- Use third person ("This skill..." not "Use this skill...")
- Keep it under 200 characters

### Content Sections

```markdown
# Skill Name

## Overview
Brief explanation of what this skill enables.

## When to Use
- Specific scenarios
- User requests that trigger this skill
- File types or tasks involved

## Workflow
Step-by-step instructions for the AI.

## Available Resources
List of scripts, references, and assets.
```

## Adding Scripts

Scripts are executable code that the AI can run:

```python
# scripts/analyze.py
#!/usr/bin/env python3
"""Analyze data and generate report."""

import sys
import json

def main():
    # Read input
    data = json.load(sys.stdin)

    # Process
    result = {"status": "success", "count": len(data)}

    # Output
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

**Supported languages:**
- Python (.py)
- Shell (.sh, .bash)
- JavaScript (.js)
- TypeScript (.ts)

## Adding References

References are documentation loaded on-demand:

```markdown
# references/api_docs.md

## API Reference

### Endpoints

- `GET /users` - List all users
- `POST /users` - Create a user
...
```

Reference these in your SKILL.md:
```markdown
For detailed API information, read `references/api_docs.md`.
```

## Adding Assets

Assets are files used in output:

```
assets/
├── report_template.md
├── logo.png
└── config.json
```

Reference these in your SKILL.md:
```markdown
Use `assets/report_template.md` as the base for the report.
```

## Example: Data Analyst Skill

```markdown
---
name: data-analyst
description: Analyze CSV data files and generate statistical insights with visualizations
---

# Data Analyst

## Overview

This skill enables analysis of CSV data with statistical summaries and insights.

## When to Use

Use this skill when the user wants to:
- Analyze CSV or tabular data
- Get statistical summaries
- Identify patterns or anomalies

## Workflow

1. Ask the user for the data file location
2. Read the file using `file_read`
3. Run `scripts/analyze.py` for statistical analysis
4. Format results using `assets/report_template.md`
5. Save the report using `file_write`

## Available Resources

### Scripts
- `scripts/analyze.py` - Statistical analysis

### Assets
- `assets/report_template.md` - Report format template

## Example Output

The analysis will include:
- Row/column counts
- Data type summary
- Missing value analysis
- Basic statistics (mean, median, std)
```

## Testing Your Skill

1. Place your skill in the skills directory
2. Start the server: `skill-mcp-server --skills-dir ./skills`
3. Use `list_skills` to verify it's loaded
4. Use `skill` to load it and test

## Tips for Effective Skills

1. **Be specific** - Clear instructions produce better results
2. **Include examples** - Show expected inputs and outputs
3. **Use scripts for reliability** - Deterministic code > AI-generated code
4. **Keep SKILL.md focused** - Move details to references/
5. **Test thoroughly** - Try edge cases before sharing

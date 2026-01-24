# Skill Format Reference

Complete specification of the skill format.

## Directory Structure

```
skill-name/
├── SKILL.md              # Required
├── scripts/              # Optional
├── references/           # Optional
├── assets/               # Optional
└── examples/             # Optional
```

## SKILL.md Specification

### Frontmatter

YAML frontmatter enclosed by `---`:

```yaml
---
name: skill-name        # Required: Unique identifier
description: ...        # Required: What the skill does
license: MIT           # Optional: License info
version: 1.0.0         # Optional: Version
author: Your Name      # Optional: Author
tags: data, analysis   # Optional: Comma-separated tags
---
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique skill identifier (lowercase, hyphens) |
| `description` | Yes | What the skill does and when to use it |
| `license` | No | License information |
| `version` | No | Semantic version |
| `author` | No | Author name/email |
| `tags` | No | Comma-separated keywords |

### Body Content

The markdown content after frontmatter contains instructions for the AI agent.

## Scripts Directory

### Supported Types

| Extension | Runtime |
|-----------|---------|
| `.py` | Python (system interpreter) |
| `.sh` | Bash |
| `.bash` | Bash |
| `.js` | Node.js |
| `.ts` | ts-node (via npx) |

### Execution

- Scripts run in the **workspace directory**
- Timeout: 120 seconds (default)
- Stdout/stderr are captured and returned

### Example Script

```python
#!/usr/bin/env python3
"""Example script with arguments."""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default='result.json')
    args = parser.parse_args()

    # Process...
    result = {"status": "success"}

    with open(args.output, 'w') as f:
        json.dump(result, f)

    print(f"Output written to {args.output}")

if __name__ == "__main__":
    main()
```

## References Directory

Documentation files loaded on-demand.

### Use Cases

- API documentation
- Schema definitions
- Detailed guides
- External references

### Example

```markdown
# references/database_schema.md

## Tables

### users
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| email | VARCHAR | Unique email |
| created_at | TIMESTAMP | Creation time |
```

## Assets Directory

Files used in output, not loaded into context.

### Use Cases

- Document templates
- Image assets
- Configuration files
- Boilerplate code

### Example Template

```markdown
# assets/report_template.md

# {{title}}

**Generated:** {{date}}

## Summary

{{summary}}

## Details

{{details}}
```

## File Restrictions

### Allowed Extensions

Reading/writing:
- `.md`, `.txt`, `.json`, `.yaml`, `.yml`
- `.py`, `.sh`, `.bash`, `.js`, `.ts`
- `.html`, `.css`, `.xml`, `.csv`, `.log`
- `.toml`, `.ini`, `.cfg`, `.conf`

### Size Limits

- Read: 1MB maximum
- Write: 100KB maximum

## Security

### Path Validation

All paths are validated to prevent directory traversal:
- Must be within skill directory (for resources)
- Must be within workspace directory (for file ops)
- Symlinks are resolved and validated

### Sandboxing

- Scripts run in workspace directory
- Cannot access files outside designated directories
- Network access depends on script implementation
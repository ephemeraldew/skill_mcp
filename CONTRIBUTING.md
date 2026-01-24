# Contributing to Skill MCP Server

Thank you for your interest in contributing to Skill MCP Server! This document provides guidelines and instructions for contributing.

## Ways to Contribute

- **Report bugs** — Open an issue describing the bug
- **Suggest features** — Open an issue with your idea
- **Submit skills** — Share your skills with the community
- **Improve documentation** — Fix typos, add examples, clarify instructions
- **Submit code** — Fix bugs or implement new features

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setting Up Your Environment

```bash
# Clone the repository
git clone https://github.com/your-org/skill-mcp-server.git
cd skill-mcp-server

# Create a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=skill_mcp_server

# Run specific test file
pytest tests/test_skill_manager.py
```

### Code Style

We use:
- **ruff** for linting and formatting
- **black** for code formatting (optional, ruff handles most)
- **mypy** for type checking (optional but recommended)

```bash
# Run linting
ruff check src/

# Auto-fix issues
ruff check src/ --fix

# Format code
ruff format src/
```

## Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, descriptive commits
3. **Add tests** for any new functionality
4. **Update documentation** if needed
5. **Run tests** and linting to ensure everything passes
6. **Submit a pull request** with a clear description

### Commit Message Format

Use clear, descriptive commit messages:

```
type: short description

Longer description if needed...
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Pull Request Description

Please include:
- **What** does this PR do?
- **Why** is this change needed?
- **How** to test the changes?
- Any **breaking changes**?

## Contributing Skills

Want to share your skills with the community? Here's how:

1. Create your skill following the [skill format](docs/skill-format.md)
2. Test it thoroughly with the MCP server
3. Open a PR adding it to the `examples/` directory
4. Include documentation in your skill's README

### Skill Quality Guidelines

- Clear, descriptive name and description
- Well-documented SKILL.md with usage examples
- Scripts should be safe and not perform destructive operations
- Include all necessary resources (templates, references)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help newcomers feel welcome

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues before creating new ones

Thank you for contributing!
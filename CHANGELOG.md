# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Skill MCP Server
- Core MCP server implementation with stdio transport
- Skill discovery and loading system
- Tools: `skill`, `list_skills`, `skill_resource`, `skill_script`
- File operations: `file_read`, `file_write`, `file_edit`
- Multi-language script execution (Python, Shell, JavaScript, TypeScript)
- Security features: path validation, file type restrictions
- Configuration via CLI arguments and environment variables
- Example skill: `skill-creator` for creating new skills

### Security
- Path traversal protection for all file operations
- File extension whitelist for read/write operations
- Script execution sandboxed to workspace directory
- Size limits for file operations

## [0.1.0] - 2025-01-24

### Added
- Initial public release
- Complete modular architecture
- Comprehensive documentation
- Example skills

---

## Version History

- `0.1.0` - Initial release with core functionality
#!/usr/bin/env python3
# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""
Skill MCP Server - Command Line Entry Point

Usage:
    python -m skill_mcp_server
    python -m skill_mcp_server --skills-dir ./my-skills --workspace ./output
    skill-mcp-server --help
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from .core.server import create_server


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="skill-mcp-server",
        description="Skill MCP Server - Turn any AI agent into a specialist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with default directories (./skills and ./workspace)
  skill-mcp-server

  # Specify custom skills directory
  skill-mcp-server --skills-dir /path/to/skills

  # Specify both directories
  skill-mcp-server --skills-dir ./my-skills --workspace ./output

  # Enable verbose logging
  skill-mcp-server -v

For more information, visit:
  https://github.com/your-org/skill-mcp-server
        """,
    )

    parser.add_argument(
        "--skills-dir",
        type=str,
        default=None,
        metavar="PATH",
        help="Directory containing skill folders (default: ./skills)",
    )

    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        metavar="PATH",
        help="Working directory for file operations (default: ./workspace)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    args = parse_args()

    # Parse paths
    skills_dir = Path(args.skills_dir) if args.skills_dir else None
    workspace_dir = Path(args.workspace) if args.workspace else None

    try:
        # Create and run server
        server = create_server(
            skills_dir=skills_dir,
            workspace_dir=workspace_dir,
            verbose=args.verbose,
        )
        asyncio.run(server.run())
        return 0

    except KeyboardInterrupt:
        # Clean exit on Ctrl+C
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

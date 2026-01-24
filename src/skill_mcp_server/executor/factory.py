# Copyright (c) 2025
# SPDX-License-Identifier: MIT

"""Executor factory for selecting the appropriate script executor."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..config.defaults import SCRIPT_TIMEOUT
from .base import BaseExecutor, ExecutionError
from .python import PythonExecutor
from .shell import ShellExecutor
from .node import NodeExecutor, TypeScriptExecutor


class ExecutorFactory:
    """Factory for creating script executors.

    Maintains a registry of executors and selects the appropriate
    one based on file extension.
    """

    def __init__(self, timeout: int = SCRIPT_TIMEOUT) -> None:
        """Initialize the factory.

        Args:
            timeout: Default timeout for executors.
        """
        self.timeout = timeout
        self._executors: list[BaseExecutor] = []
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register the default set of executors."""
        self.register(PythonExecutor(timeout=self.timeout))
        self.register(ShellExecutor(timeout=self.timeout))
        self.register(NodeExecutor(timeout=self.timeout))
        self.register(TypeScriptExecutor(timeout=self.timeout))

    def register(self, executor: BaseExecutor) -> None:
        """Register an executor.

        Args:
            executor: Executor instance to register.
        """
        self._executors.append(executor)

    def get_executor(self, path: Path) -> Optional[BaseExecutor]:
        """Get an executor that can handle the given file.

        Args:
            path: Path to the script file.

        Returns:
            Appropriate executor, or None if no executor found.
        """
        for executor in self._executors:
            if executor.can_execute(path):
                return executor
        return None

    def can_execute(self, path: Path) -> bool:
        """Check if any executor can handle the file.

        Args:
            path: Path to check.

        Returns:
            True if an executor exists for this file type.
        """
        return self.get_executor(path) is not None

    def get_supported_extensions(self) -> set[str]:
        """Get all supported file extensions.

        Returns:
            Set of supported extensions.
        """
        extensions: set[str] = set()
        for executor in self._executors:
            extensions.update(executor.extensions)
        return extensions


# Global factory instance
_factory: Optional[ExecutorFactory] = None


def get_executor_factory(timeout: int = SCRIPT_TIMEOUT) -> ExecutorFactory:
    """Get or create the global executor factory.

    Args:
        timeout: Timeout to use if creating new factory.

    Returns:
        ExecutorFactory instance.
    """
    global _factory
    if _factory is None:
        _factory = ExecutorFactory(timeout=timeout)
    return _factory


def get_executor(path: Path, timeout: int = SCRIPT_TIMEOUT) -> BaseExecutor:
    """Get an executor for the given file path.

    Args:
        path: Path to the script file.
        timeout: Execution timeout.

    Returns:
        Appropriate executor.

    Raises:
        ExecutionError: If no executor found for the file type.
    """
    factory = get_executor_factory(timeout=timeout)
    executor = factory.get_executor(path)

    if executor is None:
        supported = ", ".join(sorted(factory.get_supported_extensions()))
        raise ExecutionError(
            f"No executor found for '{path.suffix}'. "
            f"Supported types: {supported}"
        )

    return executor

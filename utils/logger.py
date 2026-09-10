"""Centralized application logging configuration."""

from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: str = "INFO") -> None:
    """Configure the root logger once for the application."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a named logger for module-level use."""
    return logging.getLogger(name or "fantasy-football-ai")

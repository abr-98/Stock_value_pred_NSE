"""
Shared logging configuration for API and MCP services.
"""
from __future__ import annotations

import logging
from typing import Optional

from apis.config import settings


def setup_logging(service_name: Optional[str] = None) -> logging.Logger:
    """Configure root logging once and return a service-scoped logger."""
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )

    logger_name = service_name or __name__
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    return logger
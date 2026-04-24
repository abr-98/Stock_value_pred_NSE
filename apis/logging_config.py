"""
Shared logging configuration for API and MCP services.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler
from typing import Optional

from apis.config import settings


_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_DIR = os.path.join(_PROJECT_ROOT, "logs", "services")
_UTILITIES_DIR = os.path.abspath(os.path.join(_PROJECT_ROOT, "utilities"))
_TRACER_INSTALLED = False


def _ensure_log_dir() -> None:
    os.makedirs(_LOG_DIR, exist_ok=True)


def _serialize_payload(payload: object, max_length: int = 5000) -> str:
    try:
        text = json.dumps(payload, default=str, ensure_ascii=True)
    except Exception:
        text = str(payload)

    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}...<truncated {len(text) - max_length} chars>"


def log_service_io(
    logger: logging.Logger,
    event: str,
    *,
    inputs: object | None = None,
    outputs: object | None = None,
    note: Optional[str] = None,
) -> None:
    """Write structured input/output logs for debugging service execution."""
    segments = [f"event={event}"]
    if note:
        segments.append(f"note={note}")
    if inputs is not None:
        segments.append(f"inputs={_serialize_payload(inputs)}")
    if outputs is not None:
        segments.append(f"outputs={_serialize_payload(outputs)}")

    logger.info(" | ".join(segments))


def setup_logging(service_name: Optional[str] = None) -> logging.Logger:
    """Configure logging and return a service-scoped logger with its own file sink."""
    _ensure_log_dir()

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger_name = service_name or __name__

    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    file_path = os.path.join(_LOG_DIR, f"{logger_name}.log")
    abs_file_path = os.path.abspath(file_path)

    has_service_file_handler = False
    for handler in logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            if os.path.abspath(getattr(handler, "baseFilename", "")) == abs_file_path:
                has_service_file_handler = True
                break

    if not has_service_file_handler:
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        logger.addHandler(file_handler)

    logger.propagate = True
    return logger


def install_utility_call_tracer(service_name: str = "service-utility-tracer") -> None:
    """Install a process-wide tracer that logs calls/returns for all utilities modules."""
    global _TRACER_INSTALLED
    if _TRACER_INSTALLED:
        return

    tracer_logger = setup_logging(service_name)

    def _tracer(frame, event, arg):  # type: ignore[no-untyped-def]
        if event not in ("call", "return"):
            return _tracer

        filename = os.path.abspath(frame.f_code.co_filename)
        if not filename.startswith(_UTILITIES_DIR):
            return _tracer

        func_name = frame.f_code.co_name
        module_name = frame.f_globals.get("__name__", "unknown")

        if event == "call":
            local_keys = list(frame.f_locals.keys())
            log_service_io(
                tracer_logger,
                "utility.trace.call",
                inputs={
                    "module": module_name,
                    "function": func_name,
                    "file": filename,
                    "line": frame.f_lineno,
                    "local_keys": local_keys[:20],
                },
            )
        else:
            log_service_io(
                tracer_logger,
                "utility.trace.return",
                outputs={
                    "module": module_name,
                    "function": func_name,
                    "file": filename,
                },
            )

        return _tracer

    sys.setprofile(_tracer)
    threading.setprofile(_tracer)
    _TRACER_INSTALLED = True
    tracer_logger.info("Installed global utility call tracer for path=%s", _UTILITIES_DIR)
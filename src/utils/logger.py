"""
Enhanced logger with file rotation and config support
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any
import sys


def setup_logger(name: str, config: Optional[Dict[str, Any]] = None) -> logging.Logger:
    """
    Setup logger with consistent formatting and optional file rotation

    Args:
        name: Logger name
        config: Optional configuration dict with logging section

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Parse config or use defaults
    if config and 'logging' in config:
        log_config = config['logging']
        level_str = log_config.get('level', 'INFO')
        log_file = log_config.get('file')
        max_size_mb = log_config.get('max_size_mb', 100)
        backup_count = log_config.get('backup_count', 5)
    else:
        level_str = 'INFO'
        log_file = None
        max_size_mb = 100
        backup_count = 5

    # Set logging level
    level = getattr(logging, level_str.upper(), logging.INFO)
    logger.setLevel(level)

    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if log file specified
    if log_file:
        try:
            # Create parent directory if it doesn't exist
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # Create rotating file handler
            max_bytes = max_size_mb * 1024 * 1024
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except (PermissionError, OSError) as e:
            # Fallback to console-only if file creation fails
            logger.warning(f"Could not create log file {log_file}: {e}. Using console logging only.")

    return logger

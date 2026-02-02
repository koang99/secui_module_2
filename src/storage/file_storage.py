"""
Local file-based storage backend
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from src.storage import StorageBackend

logger = logging.getLogger(__name__)


class FileStorage(StorageBackend):
    """File-based storage using JSON Lines format"""

    def __init__(self, output_dir: str = 'data', buffer_size: int = 100):
        """
        Initialize file storage

        Args:
            output_dir: Directory to store metrics files
            buffer_size: Number of metrics to buffer before flushing to disk
        """
        self.output_dir = Path(output_dir)
        self.buffer_size = buffer_size
        self.buffer: List[Dict[str, Any]] = []

        # Create output directory if it doesn't exist
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"File storage initialized at: {self.output_dir.absolute()}")
        except OSError as e:
            logger.error(f"Failed to create output directory {output_dir}: {e}")
            raise

    def write_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        Write metrics to storage (buffered)

        Args:
            metrics: Dictionary of metrics to store

        Returns:
            True if successful, False otherwise
        """
        try:
            # Add to buffer
            self.buffer.append(metrics)

            # Flush if buffer is full
            if len(self.buffer) >= self.buffer_size:
                self._flush()

            return True

        except Exception as e:
            logger.error(f"Error writing metrics: {e}", exc_info=True)
            return False

    def _flush(self) -> None:
        """Flush buffered metrics to file"""
        if not self.buffer:
            return

        # Get date for filename
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = self.output_dir / f'metrics-{date_str}.jsonl'

        try:
            # Append to file (create if doesn't exist)
            with open(filename, 'a', encoding='utf-8') as f:
                for metric in self.buffer:
                    json.dump(metric, f, default=str)
                    f.write('\n')

            logger.debug(f"Flushed {len(self.buffer)} metrics to {filename}")
            self.buffer.clear()

        except Exception as e:
            logger.error(f"Error flushing metrics to {filename}: {e}", exc_info=True)
            # Don't clear buffer on error - retry next time

    def query_metrics(self, metric_name: str, start_time: int, end_time: int) -> List[Dict]:
        """
        Query metrics from storage (basic implementation for Phase 1)

        Args:
            metric_name: Name of the metric to query
            start_time: Start timestamp (Unix epoch)
            end_time: End timestamp (Unix epoch)

        Returns:
            List of metric data points
        """
        # Basic implementation - not critical for Phase 1 MVP
        logger.warning("query_metrics not fully implemented in Phase 1")
        return []

    def __del__(self):
        """Flush remaining metrics on deletion"""
        try:
            self._flush()
        except Exception:
            pass  # Avoid errors during cleanup

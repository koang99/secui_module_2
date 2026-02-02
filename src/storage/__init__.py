"""
Storage backends module

Adapters for Prometheus, InfluxDB, and other time-series databases.
"""

from typing import Dict, Any, List
from abc import ABC, abstractmethod

class StorageBackend(ABC):
    """Abstract base class for storage backends"""

    @abstractmethod
    def write_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        Write metrics to storage

        Args:
            metrics: Dictionary of metrics to store

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def query_metrics(self, metric_name: str, start_time: int, end_time: int) -> List[Dict]:
        """
        Query metrics from storage

        Args:
            metric_name: Name of the metric to query
            start_time: Start timestamp (Unix epoch)
            end_time: End timestamp (Unix epoch)

        Returns:
            List of metric data points
        """
        pass

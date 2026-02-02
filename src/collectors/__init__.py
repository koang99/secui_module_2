"""
Metrics collectors module

Collectors for CPU, Memory, Disk I/O, Network, and Disk Usage metrics.
"""

from typing import Dict, Any

class BaseCollector:
    """Base class for all metric collectors"""

    def __init__(self, collection_interval: int = 10):
        """
        Initialize collector

        Args:
            collection_interval: Collection interval in seconds
        """
        self.collection_interval = collection_interval

    def collect(self) -> Dict[str, Any]:
        """
        Collect metrics

        Returns:
            Dictionary of metric name to value
        """
        raise NotImplementedError("Subclasses must implement collect()")

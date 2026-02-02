"""
Memory metrics collector using psutil
"""

import psutil
import time
import logging
from typing import Dict, Any
from src.collectors import BaseCollector

logger = logging.getLogger(__name__)


class MemoryCollector(BaseCollector):
    """Collector for memory metrics"""

    def __init__(self, collection_interval: int = 10):
        """
        Initialize memory collector

        Args:
            collection_interval: Collection interval in seconds
        """
        super().__init__(collection_interval)
        self.hostname = "localhost"  # Will be set by main agent

    def collect(self) -> Dict[str, Any]:
        """
        Collect memory metrics

        Returns:
            Dictionary containing 11 memory metrics:
            - memory_total: Total physical memory in bytes
            - memory_used: Used physical memory in bytes
            - memory_free: Free physical memory in bytes
            - memory_available: Available physical memory in bytes
            - memory_usage_percent: Memory usage percentage
            - memory_cached: Cached memory in bytes (0 on Windows)
            - memory_buffers: Buffered memory in bytes (0 on Windows)
            - swap_total: Total swap memory in bytes
            - swap_used: Used swap memory in bytes
            - swap_free: Free swap memory in bytes
            - swap_usage_percent: Swap usage percentage
        """
        metrics: Dict[str, Any] = {
            'timestamp': time.time(),
            'hostname': self.hostname
        }

        try:
            # Virtual memory (physical RAM)
            vm = psutil.virtual_memory()
            metrics['memory_total'] = vm.total
            metrics['memory_used'] = vm.used
            metrics['memory_free'] = vm.free
            metrics['memory_available'] = vm.available
            metrics['memory_usage_percent'] = vm.percent

            # Cached and buffered memory (not available on Windows)
            metrics['memory_cached'] = getattr(vm, 'cached', 0)
            metrics['memory_buffers'] = getattr(vm, 'buffers', 0)

            # Swap memory
            swap = psutil.swap_memory()
            metrics['swap_total'] = swap.total
            metrics['swap_used'] = swap.used
            metrics['swap_free'] = swap.free
            metrics['swap_usage_percent'] = swap.percent

        except Exception as e:
            logger.error(f"Error collecting memory metrics: {e}", exc_info=True)

        return metrics

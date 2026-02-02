"""
CPU metrics collector using psutil
"""

import psutil
import time
import platform
import logging
from typing import Dict, Any, Optional, List
from src.collectors import BaseCollector

logger = logging.getLogger(__name__)


class CPUCollector(BaseCollector):
    """Collector for CPU metrics"""

    def __init__(self, collection_interval: int = 10, per_core: bool = True):
        """
        Initialize CPU collector

        Args:
            collection_interval: Collection interval in seconds
            per_core: Whether to collect per-core CPU usage
        """
        super().__init__(collection_interval)
        self.per_core = per_core
        self.hostname = "localhost"  # Will be set by main agent

    def collect(self) -> Dict[str, Any]:
        """
        Collect CPU metrics

        Returns:
            Dictionary containing 9 CPU metrics:
            - cpu_usage_percent: Overall CPU usage
            - cpu_usage_per_core: List of per-core CPU usage (if enabled)
            - cpu_user_time: CPU time spent in user mode
            - cpu_system_time: CPU time spent in system mode
            - cpu_idle_time: CPU idle time
            - cpu_iowait_time: CPU time waiting for I/O (0 on Windows)
            - load_average_1m: 1-minute load average (None on Windows)
            - load_average_5m: 5-minute load average (None on Windows)
            - load_average_15m: 15-minute load average (None on Windows)
        """
        metrics: Dict[str, Any] = {
            'timestamp': time.time(),
            'hostname': self.hostname
        }

        try:
            # Overall CPU usage - use interval=1 for accurate reading
            metrics['cpu_usage_percent'] = psutil.cpu_percent(interval=1)

            # Per-core CPU usage (if enabled)
            if self.per_core:
                # Use interval=0 after the first call to avoid blocking
                per_core_usage = psutil.cpu_percent(interval=0, percpu=True)
                metrics['cpu_usage_per_core'] = per_core_usage
            else:
                metrics['cpu_usage_per_core'] = None

            # CPU times as percentages
            cpu_times = psutil.cpu_times_percent(interval=0)
            metrics['cpu_user_time'] = cpu_times.user
            metrics['cpu_system_time'] = cpu_times.system
            metrics['cpu_idle_time'] = cpu_times.idle

            # I/O wait time (not available on Windows)
            metrics['cpu_iowait_time'] = getattr(cpu_times, 'iowait', 0.0)

            # Load average (not available on Windows)
            if platform.system() != 'Windows':
                try:
                    load_avg = psutil.getloadavg()
                    metrics['load_average_1m'] = load_avg[0]
                    metrics['load_average_5m'] = load_avg[1]
                    metrics['load_average_15m'] = load_avg[2]
                except (AttributeError, OSError) as e:
                    logger.debug(f"Load average not available: {e}")
                    metrics['load_average_1m'] = None
                    metrics['load_average_5m'] = None
                    metrics['load_average_15m'] = None
            else:
                metrics['load_average_1m'] = None
                metrics['load_average_5m'] = None
                metrics['load_average_15m'] = None

        except Exception as e:
            logger.error(f"Error collecting CPU metrics: {e}", exc_info=True)

        return metrics

"""
Alerting module

Alert rules engine and notification handlers.
"""

from typing import Dict, Any
from enum import Enum

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertRule:
    """Base class for alert rules"""

    def __init__(self, name: str, severity: AlertSeverity, threshold: float):
        self.name = name
        self.severity = severity
        self.threshold = threshold

    def evaluate(self, metric_value: float) -> bool:
        """
        Evaluate if alert should be triggered

        Args:
            metric_value: Current metric value

        Returns:
            True if alert should be triggered
        """
        raise NotImplementedError("Subclasses must implement evaluate()")

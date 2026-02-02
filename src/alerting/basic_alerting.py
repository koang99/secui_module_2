"""
Basic alerting system for threshold-based alerts
"""

import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class BasicAlerting:
    """Basic threshold-based alerting engine"""

    def __init__(self, alert_rules: List[Dict[str, Any]]):
        """
        Initialize alerting system

        Args:
            alert_rules: List of alert rule dictionaries from config
        """
        self.rules = alert_rules
        self.alert_state: Dict[str, float] = {}  # {rule_name: start_time}
        logger.info(f"Initialized alerting with {len(self.rules)} rules")

    def check_rules(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check all alert rules against current metrics

        Args:
            metrics: Current metrics dictionary

        Returns:
            List of triggered alerts
        """
        triggered_alerts = []
        current_time = time.time()

        for rule in self.rules:
            alert = self._check_rule(rule, metrics, current_time)
            if alert:
                triggered_alerts.append(alert)
                # Log the alert
                self._log_alert(alert)

        return triggered_alerts

    def _check_rule(self, rule: Dict[str, Any], metrics: Dict[str, Any], current_time: float) -> Optional[Dict[str, Any]]:
        """
        Check a single alert rule

        Args:
            rule: Alert rule configuration
            metrics: Current metrics
            current_time: Current timestamp

        Returns:
            Alert dictionary if triggered, None otherwise
        """
        metric_name = rule.get('metric')
        threshold = rule.get('threshold')
        condition = rule.get('condition', '>=')
        duration = rule.get('duration', 0)
        rule_name = rule.get('name', f"Alert on {metric_name}")

        # Get metric value
        metric_value = metrics.get(metric_name)

        # Skip if metric not available
        if metric_value is None:
            return None

        # Check if threshold is exceeded
        exceeded = self._evaluate_condition(metric_value, condition, threshold)

        if exceeded:
            # Track when threshold was first exceeded
            if rule_name not in self.alert_state:
                self.alert_state[rule_name] = current_time
                logger.debug(f"Alert '{rule_name}' threshold exceeded, tracking duration")

            # Check if duration requirement is met
            time_exceeded = current_time - self.alert_state[rule_name]

            if time_exceeded >= duration:
                # Alert should be triggered
                return {
                    'name': rule_name,
                    'metric': metric_name,
                    'current_value': metric_value,
                    'threshold': threshold,
                    'condition': condition,
                    'severity': rule.get('severity', 'warning'),
                    'duration': time_exceeded,
                    'timestamp': current_time
                }
        else:
            # Threshold not exceeded - reset state if it was previously exceeded
            if rule_name in self.alert_state:
                time_exceeded = current_time - self.alert_state[rule_name]
                logger.info(f"Alert '{rule_name}' resolved after {time_exceeded:.0f}s")
                del self.alert_state[rule_name]

        return None

    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        """
        Evaluate a condition

        Args:
            value: Current metric value
            condition: Condition operator (>=, <=, >, <, ==, !=)
            threshold: Threshold value

        Returns:
            True if condition is met, False otherwise
        """
        try:
            if condition == '>=':
                return value >= threshold
            elif condition == '<=':
                return value <= threshold
            elif condition == '>':
                return value > threshold
            elif condition == '<':
                return value < threshold
            elif condition == '==':
                return value == threshold
            elif condition == '!=':
                return value != threshold
            else:
                logger.warning(f"Unknown condition operator: {condition}")
                return False
        except (TypeError, ValueError) as e:
            logger.error(f"Error evaluating condition: {e}")
            return False

    def _log_alert(self, alert: Dict[str, Any]) -> None:
        """
        Log an alert

        Args:
            alert: Alert dictionary
        """
        severity = alert['severity'].upper()
        name = alert['name']
        metric = alert['metric']
        value = alert['current_value']
        threshold = alert['threshold']
        condition = alert['condition']
        duration = alert['duration']

        # Choose log level based on severity
        if severity == 'CRITICAL':
            log_func = logger.critical
        elif severity == 'WARNING':
            log_func = logger.warning
        else:
            log_func = logger.info

        # Log the alert
        log_func(
            f"ALERT [{severity}]: {name} - {metric}={value:.2f} "
            f"(threshold: {condition} {threshold}, duration: {duration:.0f}s)"
        )

    def get_active_alerts(self) -> List[str]:
        """
        Get list of currently active alert names

        Returns:
            List of alert names that are currently in alert state
        """
        return list(self.alert_state.keys())

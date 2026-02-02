"""
CLI display module for formatting and displaying metrics
"""

import sys
from datetime import datetime
from typing import Dict, Any, Optional


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'


def display_metrics(metrics: Dict[str, Any], alert_status: Optional[Dict[str, str]] = None) -> None:
    """
    Display metrics in formatted console output

    Args:
        metrics: Dictionary of metrics to display
        alert_status: Optional dictionary of metric alerts
    """
    alert_status = alert_status or {}

    # Header
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.CYAN}System Resource Metrics{Colors.RESET}")
    print("=" * 70)

    # Timestamp and hostname
    if 'timestamp' in metrics:
        ts = datetime.fromtimestamp(metrics['timestamp'])
        print(f"Timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}")

    if 'hostname' in metrics:
        print(f"Hostname:  {metrics['hostname']}")

    print()

    # CPU Metrics Section
    if 'cpu_usage_percent' in metrics:
        print(f"{Colors.BOLD}CPU Metrics:{Colors.RESET}")

        cpu_usage = metrics['cpu_usage_percent']
        status = get_status_indicator(cpu_usage, 80, 95)
        print(f"  Usage:        {cpu_usage:6.1f}% {status}")

        # CPU times
        if all(k in metrics for k in ['cpu_user_time', 'cpu_system_time', 'cpu_idle_time']):
            print(f"  User:         {metrics['cpu_user_time']:6.1f}% | "
                  f"System: {metrics['cpu_system_time']:6.1f}% | "
                  f"Idle: {metrics['cpu_idle_time']:6.1f}%")

        # Load average (if available)
        if metrics.get('load_average_1m') is not None:
            print(f"  Load Average: {metrics['load_average_1m']:6.2f} | "
                  f"{metrics['load_average_5m']:6.2f} | "
                  f"{metrics['load_average_15m']:6.2f} (1m, 5m, 15m)")

        # Per-core usage (if available)
        if metrics.get('cpu_usage_per_core') is not None:
            per_core = metrics['cpu_usage_per_core']
            cores_str = " | ".join([f"{usage:5.1f}%" for usage in per_core[:8]])  # Show first 8 cores
            if len(per_core) > 8:
                cores_str += " | ..."
            print(f"  Per-Core:     {cores_str}")

        print()

    # Memory Metrics Section
    if 'memory_usage_percent' in metrics:
        print(f"{Colors.BOLD}Memory Metrics:{Colors.RESET}")

        mem_usage = metrics['memory_usage_percent']
        status = get_status_indicator(mem_usage, 85, 95)
        print(f"  Usage:        {mem_usage:6.1f}% {status}")

        # Memory amounts
        if 'memory_used' in metrics and 'memory_total' in metrics:
            used_gb = metrics['memory_used'] / (1024 ** 3)
            total_gb = metrics['memory_total'] / (1024 ** 3)
            free_gb = metrics.get('memory_free', 0) / (1024 ** 3)
            avail_gb = metrics.get('memory_available', 0) / (1024 ** 3)
            print(f"  Used:         {used_gb:6.2f} GB / {total_gb:6.2f} GB")
            print(f"  Available:    {avail_gb:6.2f} GB")

        # Cached and buffered (if available on Linux)
        if metrics.get('memory_cached', 0) > 0 or metrics.get('memory_buffers', 0) > 0:
            cached_gb = metrics.get('memory_cached', 0) / (1024 ** 3)
            buffers_gb = metrics.get('memory_buffers', 0) / (1024 ** 3)
            print(f"  Cached:       {cached_gb:6.2f} GB | Buffers: {buffers_gb:6.2f} GB")

        # Swap
        if 'swap_usage_percent' in metrics:
            swap_pct = metrics['swap_usage_percent']
            swap_used_mb = metrics.get('swap_used', 0) / (1024 ** 2)
            swap_total_mb = metrics.get('swap_total', 0) / (1024 ** 2)

            if swap_total_mb > 0:
                swap_status = get_status_indicator(swap_pct, 50, 80)
                print(f"  Swap:         {swap_pct:6.1f}% ({swap_used_mb:,.0f} MB / "
                      f"{swap_total_mb:,.0f} MB) {swap_status}")
            else:
                print(f"  Swap:         Not configured")

        print()

    # Footer
    print("=" * 70)
    sys.stdout.flush()


def get_status_indicator(value: float, warning_threshold: float, critical_threshold: float) -> str:
    """
    Get colored status indicator based on thresholds

    Args:
        value: Current metric value
        warning_threshold: Warning threshold
        critical_threshold: Critical threshold

    Returns:
        Colored status string
    """
    if value >= critical_threshold:
        return f"{Colors.RED}[CRITICAL]{Colors.RESET}"
    elif value >= warning_threshold:
        return f"{Colors.YELLOW}[WARNING]{Colors.RESET}"
    else:
        return f"{Colors.GREEN}[NORMAL]{Colors.RESET}"


def format_bytes(bytes_val: int, unit: str = 'auto') -> str:
    """
    Format bytes to human-readable string

    Args:
        bytes_val: Number of bytes
        unit: Target unit ('auto', 'KB', 'MB', 'GB', 'TB')

    Returns:
        Formatted string
    """
    if unit == 'auto':
        for unit_name in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit_name}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"
    else:
        divisors = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
        divisor = divisors.get(unit, 1)
        return f"{bytes_val / divisor:.2f} {unit}"

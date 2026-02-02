"""
Unit tests for CPU collector
"""

import pytest
import time
from src.collectors.cpu_collector import CPUCollector


def test_cpu_collector_initialization():
    """Test CPU collector initializes correctly"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    assert collector.collection_interval == 10
    assert collector.per_core is False
    assert collector.hostname == "localhost"


def test_cpu_collector_with_per_core():
    """Test CPU collector with per-core enabled"""
    collector = CPUCollector(collection_interval=10, per_core=True)
    assert collector.per_core is True


def test_cpu_collect_returns_dict():
    """Test that collect() returns a dictionary"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    collector.hostname = 'test-host'
    metrics = collector.collect()

    assert isinstance(metrics, dict)
    assert metrics['hostname'] == 'test-host'


def test_cpu_metrics_present():
    """Test that all required CPU metrics are present"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    collector.hostname = 'test-host'
    metrics = collector.collect()

    # Check all required keys are present
    required_keys = [
        'timestamp',
        'hostname',
        'cpu_usage_percent',
        'cpu_usage_per_core',
        'cpu_user_time',
        'cpu_system_time',
        'cpu_idle_time',
        'cpu_iowait_time',
        'load_average_1m',
        'load_average_5m',
        'load_average_15m'
    ]

    for key in required_keys:
        assert key in metrics, f"Missing metric: {key}"


def test_cpu_usage_percent_range():
    """Test that CPU usage percent is in valid range"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    metrics = collector.collect()

    cpu_usage = metrics['cpu_usage_percent']
    assert isinstance(cpu_usage, (int, float))
    assert 0 <= cpu_usage <= 100, f"CPU usage {cpu_usage} outside valid range 0-100"


def test_cpu_per_core_enabled():
    """Test that per-core metrics are collected when enabled"""
    collector = CPUCollector(collection_interval=10, per_core=True)
    metrics = collector.collect()

    per_core = metrics['cpu_usage_per_core']
    assert per_core is not None
    assert isinstance(per_core, list)
    assert len(per_core) > 0, "Expected at least one CPU core"

    # Each core usage should be in valid range
    for i, usage in enumerate(per_core):
        assert isinstance(usage, (int, float))
        assert 0 <= usage <= 100, f"Core {i} usage {usage} outside valid range"


def test_cpu_per_core_disabled():
    """Test that per-core metrics are None when disabled"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    metrics = collector.collect()

    assert metrics['cpu_usage_per_core'] is None


def test_cpu_times_are_numeric():
    """Test that CPU time metrics are numeric"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    metrics = collector.collect()

    time_metrics = ['cpu_user_time', 'cpu_system_time', 'cpu_idle_time', 'cpu_iowait_time']
    for metric in time_metrics:
        value = metrics[metric]
        assert isinstance(value, (int, float)), f"{metric} should be numeric"
        assert value >= 0, f"{metric} should be non-negative"


def test_cpu_timestamp_is_recent():
    """Test that timestamp is recent"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    before = time.time()
    metrics = collector.collect()
    after = time.time()

    timestamp = metrics['timestamp']
    assert isinstance(timestamp, (int, float))
    assert before <= timestamp <= after + 1, "Timestamp not within expected range"


def test_cpu_hostname_can_be_set():
    """Test that hostname can be customized"""
    collector = CPUCollector(collection_interval=10, per_core=False)
    collector.hostname = 'custom-host'
    metrics = collector.collect()

    assert metrics['hostname'] == 'custom-host'


def test_cpu_collector_handles_errors_gracefully():
    """Test that collector doesn't crash on errors"""
    collector = CPUCollector(collection_interval=10, per_core=False)

    # Even if psutil has issues, collect should return a dict with at least timestamp and hostname
    try:
        metrics = collector.collect()
        assert isinstance(metrics, dict)
        assert 'timestamp' in metrics
        assert 'hostname' in metrics
    except Exception as e:
        pytest.fail(f"Collector should not raise exceptions, but got: {e}")

"""
Unit tests for Memory collector
"""

import pytest
import time
from src.collectors.memory_collector import MemoryCollector


def test_memory_collector_initialization():
    """Test memory collector initializes correctly"""
    collector = MemoryCollector(collection_interval=10)
    assert collector.collection_interval == 10
    assert collector.hostname == "localhost"


def test_memory_collect_returns_dict():
    """Test that collect() returns a dictionary"""
    collector = MemoryCollector(collection_interval=10)
    collector.hostname = 'test-host'
    metrics = collector.collect()

    assert isinstance(metrics, dict)
    assert metrics['hostname'] == 'test-host'


def test_memory_metrics_present():
    """Test that all required memory metrics are present"""
    collector = MemoryCollector(collection_interval=10)
    collector.hostname = 'test-host'
    metrics = collector.collect()

    # Check all required keys are present
    required_keys = [
        'timestamp',
        'hostname',
        'memory_total',
        'memory_used',
        'memory_free',
        'memory_available',
        'memory_usage_percent',
        'memory_cached',
        'memory_buffers',
        'swap_total',
        'swap_used',
        'swap_free',
        'swap_usage_percent'
    ]

    for key in required_keys:
        assert key in metrics, f"Missing metric: {key}"


def test_memory_values_are_numeric():
    """Test that memory metrics are numeric"""
    collector = MemoryCollector(collection_interval=10)
    metrics = collector.collect()

    numeric_metrics = [
        'memory_total', 'memory_used', 'memory_free', 'memory_available',
        'memory_cached', 'memory_buffers',
        'swap_total', 'swap_used', 'swap_free'
    ]

    for metric in numeric_metrics:
        value = metrics[metric]
        assert isinstance(value, (int, float)), f"{metric} should be numeric"
        assert value >= 0, f"{metric} should be non-negative"


def test_memory_usage_percent_range():
    """Test that memory usage percent is in valid range"""
    collector = MemoryCollector(collection_interval=10)
    metrics = collector.collect()

    mem_usage = metrics['memory_usage_percent']
    assert isinstance(mem_usage, (int, float))
    assert 0 <= mem_usage <= 100, f"Memory usage {mem_usage} outside valid range 0-100"

    swap_usage = metrics['swap_usage_percent']
    assert isinstance(swap_usage, (int, float))
    assert 0 <= swap_usage <= 100, f"Swap usage {swap_usage} outside valid range 0-100"


def test_memory_total_greater_than_used():
    """Test that total memory is greater than or equal to used memory"""
    collector = MemoryCollector(collection_interval=10)
    metrics = collector.collect()

    assert metrics['memory_total'] >= metrics['memory_used'], \
        "Total memory should be >= used memory"

    if metrics['swap_total'] > 0:
        assert metrics['swap_total'] >= metrics['swap_used'], \
            "Total swap should be >= used swap"


def test_memory_timestamp_is_recent():
    """Test that timestamp is recent"""
    collector = MemoryCollector(collection_interval=10)
    before = time.time()
    metrics = collector.collect()
    after = time.time()

    timestamp = metrics['timestamp']
    assert isinstance(timestamp, (int, float))
    assert before <= timestamp <= after + 1, "Timestamp not within expected range"


def test_memory_hostname_can_be_set():
    """Test that hostname can be customized"""
    collector = MemoryCollector(collection_interval=10)
    collector.hostname = 'custom-host'
    metrics = collector.collect()

    assert metrics['hostname'] == 'custom-host'


def test_memory_available_is_reasonable():
    """Test that available memory is reasonable"""
    collector = MemoryCollector(collection_interval=10)
    metrics = collector.collect()

    # Available should be <= total
    assert metrics['memory_available'] <= metrics['memory_total'], \
        "Available memory should be <= total memory"

    # Available should be >= 0
    assert metrics['memory_available'] >= 0, \
        "Available memory should be non-negative"


def test_memory_collector_handles_errors_gracefully():
    """Test that collector doesn't crash on errors"""
    collector = MemoryCollector(collection_interval=10)

    # Even if psutil has issues, collect should return a dict with at least timestamp and hostname
    try:
        metrics = collector.collect()
        assert isinstance(metrics, dict)
        assert 'timestamp' in metrics
        assert 'hostname' in metrics
    except Exception as e:
        pytest.fail(f"Collector should not raise exceptions, but got: {e}")

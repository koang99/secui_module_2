# Configuration

This directory contains configuration files for the metrics collection system.

## Files

- `config.yaml` - Main configuration file
  - Agent settings (hostname, collection interval, port)
  - Collector configurations (CPU, memory, disk, network)
  - Storage backend settings (Prometheus, InfluxDB, TimescaleDB)
  - Alert rules and thresholds
  - Notification channels
  - Logging configuration

## Usage

Copy `config.yaml` to your deployment location and modify the values according to your environment:

```bash
cp config/config.yaml /etc/metrics-collector/config.yaml
```

## Environment Variables

Configuration values can be overridden using environment variables:

- `METRICS_HOSTNAME` - Override agent hostname
- `METRICS_PORT` - Override export port
- `METRICS_INTERVAL` - Override collection interval
- `PROMETHEUS_PUSHGATEWAY` - Prometheus push gateway URL
- `INFLUXDB_URL` - InfluxDB server URL
- `INFLUXDB_TOKEN` - InfluxDB authentication token

## Configuration Validation

Run the following command to validate your configuration:

```bash
python -m src.utils.config_validator config/config.yaml
```

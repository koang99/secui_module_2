# Dashboards

Grafana dashboard definitions for visualizing system metrics.

## Planned Dashboards

### 1. System Overview Dashboard
- CPU usage (overall and per-core)
- Memory usage
- Disk I/O throughput
- Network bandwidth
- Disk space usage

### 2. CPU Metrics Dashboard
- CPU usage percent (timeline)
- Per-core CPU usage (heatmap)
- Load averages (1m, 5m, 15m)
- CPU time breakdown (user, system, idle, iowait)

### 3. Memory Metrics Dashboard
- Memory usage percent (timeline)
- Memory breakdown (used, cached, buffers, free)
- Swap usage
- Top memory-consuming processes

### 4. Disk I/O Dashboard
- Read/Write throughput (bytes/s)
- Read/Write IOPS
- I/O wait time
- Disk queue length
- I/O utilization percent

### 5. Network Dashboard
- Bytes sent/received (timeline)
- Packets sent/received
- Network errors and drops
- Bandwidth usage percent
- Active connections

### 6. Alerts Dashboard
- Active alerts
- Alert history
- Alert trends
- Time to resolution

## File Format

Dashboards will be exported as JSON files from Grafana and stored here for version control and easy deployment.

## Import Instructions

1. Open Grafana UI
2. Navigate to Dashboards → Import
3. Upload the JSON file
4. Select Prometheus data source
5. Click Import

## Export Instructions

1. Open the dashboard in Grafana
2. Click the share icon (top right)
3. Select "Export" tab
4. Click "Save to file"
5. Move the JSON file to this directory

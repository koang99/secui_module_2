# System Resource Metrics Collection System

A high-performance server monitoring system that collects and analyzes system resource metrics in real-time.

## Features

- **Real-time Monitoring**: Collects metrics every 10 seconds
- **5 Core Metrics**: CPU, Memory, Disk I/O, Network, Disk Usage
- **Low Overhead**: <5% CPU, <100MB memory usage
- **Flexible Storage**: Supports Prometheus, InfluxDB, TimescaleDB
- **Smart Alerting**: Configurable thresholds with multi-channel notifications
- **Scalable**: Designed to monitor 1,000+ servers

## Quick Start

### Prerequisites

Choose your implementation language:

**Python:**
```bash
pip install psutil prometheus-client
```

**Go:**
```bash
go get github.com/shirou/gopsutil/v3
```

**Node.js:**
```bash
npm install systeminformation
```

### Installation

```bash
git clone <repository-url>
cd new_test
```

### Configuration

Edit `config/config.yml`:

```yaml
collection:
  interval: 10s

storage:
  type: prometheus
  endpoint: http://localhost:9090

alerts:
  cpu_warning: 80
  cpu_critical: 95
  memory_warning: 85
  memory_critical: 95
```

## Architecture

See `CLAUDE.md` for detailed architecture documentation.

```
[Server] → [Agent] → [Storage] → [Dashboard]
                         ↓
                    [Alerting]
```

## Documentation

- **PRD**: Full requirements in `docs/README.md`
- **Development Guide**: See `CLAUDE.md`
- **API Documentation**: Coming in Phase 3

## Project Status

**Current Phase**: Phase 1 (MVP)

- [ ] CPU collector
- [ ] Memory collector
- [ ] Local file storage
- [ ] CLI output
- [ ] Basic alerts

## Contributing

This project follows the implementation phases defined in `docs/README.md`.

## License

MIT

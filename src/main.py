"""
Main entry point for the metrics collection agent
"""

import argparse
import sys
import signal
import time
from pathlib import Path

from src.utils import setup_logger
from src.utils.config_loader import load_config
from src.collectors.cpu_collector import CPUCollector
from src.collectors.memory_collector import MemoryCollector
from src.storage.file_storage import FileStorage
from src.alerting.basic_alerting import BasicAlerting
from src.cli import display_metrics

# Initialize logger (will be reconfigured with config file)
logger = setup_logger(__name__)


class MetricsAgent:
    """Main metrics collection agent"""

    def __init__(self, config_path: str):
        """
        Initialize the metrics agent

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.running = False

        # Load configuration
        self.config = load_config(config_path)

        # Setup logger with config
        global logger
        logger = setup_logger(__name__, self.config)
        logger.info(f"Initializing metrics agent with config: {config_path}")

        # Get agent settings
        self.hostname = self.config['agent']['hostname']
        self.collection_interval = self.config['agent']['collection_interval']

        # Initialize collectors
        self.collectors = {}

        # CPU collector
        cpu_config = self.config['collectors']['cpu']
        if cpu_config['enabled']:
            self.collectors['cpu'] = CPUCollector(
                collection_interval=cpu_config['interval'],
                per_core=cpu_config['per_core']
            )
            self.collectors['cpu'].hostname = self.hostname
            logger.info("CPU collector initialized")

        # Memory collector
        mem_config = self.config['collectors']['memory']
        if mem_config['enabled']:
            self.collectors['memory'] = MemoryCollector(
                collection_interval=mem_config['interval']
            )
            self.collectors['memory'].hostname = self.hostname
            logger.info("Memory collector initialized")

        # Initialize storage
        self.storage = FileStorage(output_dir='data')

        # Initialize alerting
        if self.config['alerts']['enabled']:
            self.alerting = BasicAlerting(self.config['alerts']['rules'])
        else:
            self.alerting = None

        logger.info("Metrics agent initialized successfully")

    def start(self):
        """Start the metrics collection agent"""
        logger.info("Starting metrics collection agent...")
        self.running = True

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            while self.running:
                # Collect metrics from all enabled collectors
                metrics = {
                    'timestamp': time.time(),
                    'hostname': self.hostname
                }

                # CPU metrics
                if 'cpu' in self.collectors:
                    logger.debug("Collecting CPU metrics...")
                    cpu_metrics = self.collectors['cpu'].collect()
                    # Merge CPU metrics (skip timestamp and hostname to avoid overwriting)
                    for key, value in cpu_metrics.items():
                        if key not in ['timestamp', 'hostname']:
                            metrics[key] = value

                # Memory metrics
                if 'memory' in self.collectors:
                    logger.debug("Collecting memory metrics...")
                    memory_metrics = self.collectors['memory'].collect()
                    # Merge memory metrics
                    for key, value in memory_metrics.items():
                        if key not in ['timestamp', 'hostname']:
                            metrics[key] = value

                # Store metrics
                if metrics:
                    logger.debug("Storing metrics...")
                    self.storage.write_metrics(metrics)

                    # Check alerts
                    if self.alerting:
                        alerts = self.alerting.check_rules(metrics)
                        # Alerts are already logged by the alerting system

                    # Display metrics
                    display_metrics(metrics)

                # Sleep until next collection
                time.sleep(self.collection_interval)

        except Exception as e:
            logger.error(f"Error in collection loop: {e}", exc_info=True)
            sys.exit(1)

        finally:
            # Flush any buffered metrics
            logger.info("Flushing remaining metrics...")
            if hasattr(self.storage, '_flush'):
                self.storage._flush()

    def stop(self):
        """Stop the metrics collection agent"""
        logger.info("Stopping metrics collection agent...")
        self.running = False

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="System Resource Metrics Collection Agent"
    )
    parser.add_argument(
        "-c", "--config",
        default="config/config.yaml",
        help="Path to configuration file (default: config/config.yaml)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging level
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)

    # Check if config file exists
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found: {args.config}")
        sys.exit(1)

    # Create and start agent
    agent = MetricsAgent(str(config_path))
    agent.start()


if __name__ == "__main__":
    main()

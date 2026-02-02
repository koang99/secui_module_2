"""
Main entry point for the metrics collection agent
"""

import argparse
import sys
import signal
import time
from pathlib import Path

from src.utils import setup_logger

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
        logger.info(f"Initializing metrics agent with config: {config_path}")

    def start(self):
        """Start the metrics collection agent"""
        logger.info("Starting metrics collection agent...")
        self.running = True

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            while self.running:
                # TODO: Implement collection loop
                logger.debug("Collection cycle...")
                time.sleep(10)

        except Exception as e:
            logger.error(f"Error in collection loop: {e}", exc_info=True)
            sys.exit(1)

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

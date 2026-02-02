"""
Configuration file loader and validator
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load and validate configuration from YAML file

    Args:
        config_path: Path to configuration file

    Returns:
        Parsed configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid or missing required sections
        yaml.YAMLError: If YAML parsing fails
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # Load YAML file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse YAML config: {e}")

    if config is None:
        raise ValueError("Config file is empty")

    # Validate required sections
    required_sections = ['agent', 'collectors', 'storage', 'alerts', 'logging']
    missing_sections = [section for section in required_sections if section not in config]

    if missing_sections:
        raise ValueError(f"Missing required config sections: {', '.join(missing_sections)}")

    # Validate agent section
    if 'hostname' not in config['agent']:
        raise ValueError("Missing required 'hostname' in agent section")
    if 'collection_interval' not in config['agent']:
        raise ValueError("Missing required 'collection_interval' in agent section")

    # Validate collectors section has at least CPU and Memory
    if 'cpu' not in config['collectors']:
        raise ValueError("Missing 'cpu' in collectors section")
    if 'memory' not in config['collectors']:
        raise ValueError("Missing 'memory' in collectors section")

    # Validate alerts section
    if 'enabled' not in config['alerts']:
        raise ValueError("Missing 'enabled' in alerts section")
    if 'rules' not in config['alerts']:
        raise ValueError("Missing 'rules' in alerts section")

    # Validate logging section
    if 'level' not in config['logging']:
        raise ValueError("Missing 'level' in logging section")

    return config

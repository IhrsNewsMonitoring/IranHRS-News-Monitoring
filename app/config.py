"""Configuration loading utilities.

This module provides a function to load YAML configuration files
used by the monitoring system. The configuration defines API
credentials for Telegram, a list of channels and websites to
monitor, and the path to the SQLite database.
"""

from pathlib import Path
from typing import Any, Dict
import yaml


def load_config(path: str) -> Dict[str, Any]:
    """Load a YAML configuration file.

    Parameters
    ----------
    path : str
        Path to the YAML configuration file.

    Returns
    -------
    Dict[str, Any]
        Dictionary representation of the configuration.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
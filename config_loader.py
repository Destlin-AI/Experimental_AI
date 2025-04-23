from core.config_loader import get
"""
LOGICSHREDDER :: config_loader.py
Purpose: Load and access system_config.yaml safely and globally
"""

import yaml
from pathlib import Path

CONFIG_PATH = Path("configs/system_config.yaml")
_config_cache = {}

def load_config():
    global _config_cache
    if _config_cache:
        return _config_cache
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            _config_cache = yaml.safe_load(f)
            return _config_cache
    except Exception as e:
        print(f"[config_loader] ERROR Failed to load config: {e}")
        return {}

def get(path, default=None):
    """Get config value by dot.path string (e.g. 'tuning.decay_rate')"""
    keys = path.split(".")
    val = load_config()
    for key in keys:
        if isinstance(val, dict):
            val = val.get(key)
        else:
            return default
    return val if val is not None else default

# [CONFIG_PATCHED]

#!/usr/bin/env python3
import json
import os
from pathlib import Path
from .helper.config import config

API_URL = os.getenv('TURBO_API')
TEAM = os.getenv('TURBO_TEAM')


def run():
    """Setup turbo cache configuration."""
    turbo_folder_path = config['ROOT_PATH'] / '.turbo'
    config_file_path = turbo_folder_path / 'config.json'
    
    # Create turbo folder if it doesn't exist
    if not turbo_folder_path.exists():
        turbo_folder_path.mkdir(parents=True, exist_ok=True)
    
    # Write config file
    config_data = {
        'teamid': TEAM,
        'apiurl': API_URL,
    }
    
    with open(config_file_path, 'w') as f:
        json.dump(config_data, f, indent=2)


if __name__ == "__main__":
    run()

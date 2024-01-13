import os
import yaml
from pathlib import Path


def load_config():
    script_path = Path(__file__).parent
    filename = 'application.yaml'
    env = os.getenv('active_env')
    if env is not None and env not in ['', 'None']:
        filename = f'application_{env}.yaml'

    yaml_file_path = script_path.parent / 'conf' / filename
    with open(yaml_file_path, 'r', encoding='UTF-8') as file:
        config = yaml.safe_load(file)
    return config


application_config = load_config()

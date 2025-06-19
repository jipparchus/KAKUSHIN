import yaml
import os


def load_config():
    config_file = 'config.yaml'
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


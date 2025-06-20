import yaml
import os


def load_config():
    # Set the default path to the config file. If not defined, return the second argument.
    # This is set to prevent the test code from reading the production config file.
    config_path = os.getenv(
        'CONFIG_PATH',
        os.path.join(os.path.dirname(__file__), 'config.yaml')
    )
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

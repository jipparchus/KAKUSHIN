import os
from unittest import mock


def test_load_config():
    mock.patch.stopall()  # cancel the global mock from conftest.py
    # Patch the CONFIG_PATH environment variable
    os.environ["CONFIG_PATH"] = str(os.path.join(os.path.dirname(__file__).replace('tests', 'backend'), 'config_template.yaml'))
    from backend.config import load_config
    config = load_config()
    # Type check
    assert isinstance(config, dict)

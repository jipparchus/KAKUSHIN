import os


def test_load_config():
    from unittest import mock
    mock.patch.stopall()  # cancel the global mock from conftest.py

    # Patch the CONFIG_PATH environment variable
    print('CURRENT DIR: ')
    print(os.path.join(os.path.dirname(__file__)))
    os.environ["CONFIG_PATH"] = str(os.path.join(os.path.dirname(__file__).replace('tests', 'backend'), 'config_template.yaml'))
    from backend.config import load_config
    config = load_config()
    # Type check
    assert isinstance(config, dict)

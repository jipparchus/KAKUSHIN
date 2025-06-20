def test_load_config():
    from unittest import mock
    mock.patch.stopall()  # cancel the global mock from conftest.py

    from backend.config import load_config
    config = load_config()
    # Type check
    assert isinstance(config, dict)

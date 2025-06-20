import os
import pytest
from unittest import mock

from backend.db.init_rdb import main


@pytest.fixture
def test_config(tmp_path):
    """
    temp DB file for testing
    This is a function used for temporary patch of the load_config with various configurations
    """
    db_path = tmp_path / 'test_database_temp.db'
    return {
        'paths': {
            'database': str(db_path)}
    }


# 1. Database already exists
def test_main_db_exists(tmp_path, test_config):
    assert not os.path.exists(test_config['path']['database'])
    # Temporary patch load_config with various configurations
    with mock.patch('backend.config.load_config', return_value=test_config):
        report = main()
        assert isinstance(report, dict)
        assert report['message'] == 'Database already exists. Skipping initialization.'
        assert report['db_path'] == test_config['paths']['database']


# 2. Database created successfully




# 3. Exception during creation of database
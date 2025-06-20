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
    db_path = test_config['paths']['database']
    # Create a temporary file to simulate an existing file
    open(db_path, 'w').close()
    # Temporary patch for load_config
    with mock.patch('backend.db.init_rdb.config.load_config', return_value=test_config):
        report = main()
        assert os.path.exists(db_path)
        assert isinstance(report, dict)
        assert report['message'] == 'Database already exists. Skipping initialization.'
        assert report['db_path'] == db_path
        # Clean up the file
        os.remove(db_path)


# 2. Database created successfully
def test_main_db_created(tmp_path, test_config):
    db_path = test_config['paths']['database']
    assert not os.path.exists(db_path)
    # Temporary patch for load_config
    with mock.patch('backend.db.init_rdb.config.load_config', return_value=test_config):
        report = main()
        assert isinstance(report, dict)
        assert report['message'] == 'Database created successfully.'
        assert report['db_path'] == db_path
        os.remove(db_path)


# 3. Exception during creation of database
def test_main_db_exception(tmp_path, test_config):
    assert not os.path.exists(test_config['paths']['database'])
    # Temporary patch for load_config
    with mock.patch('backend.db.init_rdb.config.load_config', return_value=test_config), \
            mock.patch('backend.db.init_rdb.get_engine', side_effect=Exception('engine fault')):
        report = main()
        assert isinstance(report, dict)
        assert 'engine fault' in report['message']
        assert report['db_path'] is None

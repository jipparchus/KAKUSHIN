import os
import pytest
from unittest import mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.init_rdb import main


@pytest.fixture(autouse=True)
def tmp_config():
    """
    temp DB file for testing
    This is a function used for temporary patch of the load_config with various configurations
    """
    mock.patch.stopall()
    db_path = 'test_database_temp.db'
    return {
        'paths': {
            'database': db_path},
        'database': {
            'uri': f'sqlite:///:memory:{db_path}',
        }
    }


# @pytest.fixture()
# def tmp_get_engine():

# @pytest.fixture
# def tmp_get_engine(tmp_config):
#     config = tmp_config()
#     engine = create_engine(
#         config['database']['uri'],
#         connect_args={'check_same_thread': False},  # required for sqlite
#         poolclass=StaticPool,  # Needed to persist DB across sessions
#         echo=False,
#         )
#     return engine


# 1. Database already exists
@pytest.mark.no_mock_config
def test_main_db_exists(tmp_config):
    config = tmp_config
    db_path = config['paths']['database']
    # Create a temporary file to simulate an existing file
    open(db_path, 'w').close()
    # Temporary patch for load_config
    with mock.patch('backend.db.init_rdb.config.load_config', return_value=tmp_config):
        report = main()
        assert os.path.exists(db_path)
        assert isinstance(report, dict)
        assert report['message'] == 'Database already exists. Skipping initialization.'
        assert report['db_path'] == db_path
        # Clean up the file
        os.remove(db_path)


# 2. Database created successfully
@pytest.mark.no_mock_config
def test_main_db_created(tmp_config):
    config = tmp_config
    db_path = config['paths']['database']
    assert not os.path.exists(db_path)
    # Temporary patch for load_config
    with mock.patch('backend.db.init_rdb.config.load_config', return_value=tmp_config):
        report = main()
        assert isinstance(report, dict)
        assert report['message'] == 'Database created successfully.'
        assert report['db_path'] == db_path
        os.remove(db_path)


# 3. Exception during creation of database
@pytest.mark.no_mock_config
def test_main_db_exception(tmp_config):
    config = tmp_config
    assert not os.path.exists(config['paths']['database'])
    # Temporary patch for load_config
    with mock.patch('backend.db.init_rdb.config.load_config', return_value=tmp_config), \
            mock.patch('backend.db.init_rdb.get_engine', side_effect=Exception('engine fault')):
        report = main()
        assert isinstance(report, dict)
        assert 'engine fault' in report['message']
        assert report['db_path'] is None

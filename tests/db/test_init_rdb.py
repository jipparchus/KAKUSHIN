import os
import pytest
from unittest import mock


@pytest.fixture(autouse=True)
def tmp_config(mocker):
    """
    temp DB file for testing
    This is a function used for temporary patch of the load_config with various configurations
    """
    db_path = 'test_database_temp.db'
    fake_config = {
            'paths': {
                'database': db_path},
            'database': {
                'uri': f'sqlite:///:memory:{db_path}',
            }
        }
    patch_paths = [
        'backend.db.init_rdb.config.load_config',
        'backend.db.session.load_config',
    ]
    patches = {}
    for path in patch_paths:
        mock = mocker.patch(path)
        mock.return_value = fake_config
        patches[path] = mock
    yield patches


# 1. Database already exists
@pytest.mark.no_mock_config
def test_main_db_exists():
    from backend.db.init_rdb import main
    from backend import config
    config_dict = config.load_config()
    db_path = config_dict['paths']['database']
    # Create a temporary file to simulate an existing file
    open(db_path, 'w').close()
    report = main()
    assert os.path.exists(db_path)
    assert isinstance(report, dict)
    assert report['message'] == 'Database already exists. Skipping initialization.'
    assert report['db_path'] == db_path
    # Clean up the file
    os.remove(db_path)


# 2. Database created successfully
@pytest.mark.no_mock_config
def test_main_db_created():
    from backend.db.init_rdb import main
    from backend import config
    config_dict = config.load_config()
    db_path = config_dict['paths']['database']
    assert not os.path.exists(db_path)
    report = main()
    assert isinstance(report, dict)
    assert report['message'] == 'Database created successfully.'
    assert report['db_path'] == db_path


# 3. Exception during creation of database
@pytest.mark.no_mock_config
def test_main_db_exception():
    from backend.db.init_rdb import main
    from backend import config
    config_dict = config.load_config()
    db_path = config_dict['paths']['database']
    assert not os.path.exists(db_path)
    # Temporary patch for load_config
    with mock.patch('backend.db.init_rdb.get_engine', side_effect=Exception('engine fault')):
        report = main()
        assert isinstance(report, dict)
        assert 'engine fault' in report['message']
        assert report['db_path'] is None

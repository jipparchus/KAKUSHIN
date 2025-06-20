"""
Create a SQLite database based on /models.py
"""
import os
from backend import config

# DATABASE MODELS
from backend.db.models import Base
from backend.db.session import get_engine


def main():
    report = {}
    report['db_path'] = None
    config_dict = config.load_config()
    if os.path.exists(config_dict['paths']['database']):
        report['message'] = 'Database already exists. Skipping initialization.'
        report['db_path'] = config_dict['paths']['database']
    else:
        try:
            engine = get_engine()
            # CREATE TABLES
            Base.metadata.create_all(engine)
            report['message'] = 'Database created successfully.'
            report['db_path'] = str(engine.url)
        except Exception as e:
            report['message'] = str(e)
    return report


if __name__ == '__main__':
    main()

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
    db_path = config_dict['paths']['database']
    if os.path.exists(db_path):
        report['message'] = 'Database already exists. Skipping initialization.'
        report['db_path'] = db_path
    else:
        try:
            engine = get_engine()
            # CREATE TABLES
            Base.metadata.create_all(engine)
            report['message'] = 'Database created successfully.'
            report['db_path'] = db_path  # slightly different from engine.url
        except Exception as e:
            report['message'] = str(e)
    return report

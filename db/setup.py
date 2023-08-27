"""
    @File: model.py
    @Author: Ashikur Rahman
    @Description: Provides db setup related utilities
"""

from db.model import Settings
from db.controller import DbSession

default_settings = [
    Settings(key = 'BASE_DIR', default = ''),
    Settings(key = 'HTTP_REQUEST_TIMEOUT', default = '5')
]

def add_default_settings():
    """Add default settings to db"""
    with DbSession() as session:
        for setting in default_settings:
            session.add(setting)

            try:
                session.commit()
            except:
                # setting already exists
                session.rollback()

def initial_db_setup():
    add_default_settings()

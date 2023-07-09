"""
    @File: model.py
    @Author: Ashikur Rahman
    @Description: Provides db setup related utilities
"""

import os
import subprocess
import functools
from db.model import Settings
from db.controller import DbSession


def upgrade_db():
    curr_dir = os.getcwd()
    db_dir = os.path.dirname(__file__)

    os.chdir(db_dir)
    subprocess.run(["alembic", "upgrade", "head"], stderr=subprocess.DEVNULL)
    os.chdir(curr_dir)

def downgrade_db():
    curr_dir = os.getcwd()
    db_dir = os.path.dirname(__file__)

    os.chdir(db_dir)
    subprocess.run(["alembic", "downgrade", "base"], stderr=subprocess.DEVNULL)
    os.chdir(curr_dir)


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
    upgrade_db()
    add_default_settings()

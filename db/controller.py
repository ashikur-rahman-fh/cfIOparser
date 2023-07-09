"""
    @File: controller.py
    @Author: Ashikur Rahman
    @Description: Provides db utilities like reading and writing to db
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.config import db_conn_str
from db.model import Settings

class DbSession:
    """SQLAlchemy session to perform query in the db"""
    def __init__(self) -> None:
        self.engine = create_engine(db_conn_str, echo=False)

    def __enter__(self):
        self.session = Session(self.engine)
        return self.session

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.close()

def add_setting(key, value):
    """Add setting api"""
    with DbSession() as session:
        old_setting = session.query(Settings).filter(Settings.key == key).scalar()

        if not old_setting:
            new_setting = Settings(key = key, custom = value)
            session.add(new_setting)
        else:
            old_setting.custom = value

        session.commit()

def get_setting(key):
    """get setting api"""
    with DbSession() as session:
        setting = session.query(Settings).filter(Settings.key == key).scalar()

    return setting

def get_setting_value(key):
    """get the setting value that can be work with"""
    setting = get_setting(key=key)

    if not setting:
        return None
    elif setting.custom:
        return setting.custom
    return setting.default

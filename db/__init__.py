import os

from .config import db_path
from .saengine import engine, Base
from .model import Settings

dir_name = os.path.dirname(db_path)
if not os.path.exists(dir_name):
    os.makedirs(dir_name, exist_ok=True)

Base.metadata.create_all(bind=engine.connect(), tables=[Settings.__table__], checkfirst=True)

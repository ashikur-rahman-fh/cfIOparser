
from db.config import db_conn_str
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(db_conn_str, echo=False)
Base = declarative_base()

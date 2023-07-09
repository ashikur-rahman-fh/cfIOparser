"""
    @File: model.py
    @Author: Ashikur Rahman
    @Description: DB models that represents db table
"""

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Settings(Base):
    __tablename__ = "settings"

    key = Column(String(50), primary_key=True)
    default = Column(String(500))
    custom = Column(String(500))

    def __repr__(self):
        return f"{self.key} -> {self.default} | {self.custom}"

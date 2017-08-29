from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Integer, DateTime

from {{cookiecutter.module_name}} import utils


BASE = declarative_base()


class User(BASE):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    created_at = Column(DateTime, default=lambda: utils.now())

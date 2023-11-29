from datetime import datetime
from typing import Any

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from settings import config


db = SqliteDatabase(config.database, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()
    queries: Any


class History(BaseModel):
    user = ForeignKeyField(model=User, backref="queries")
    query = CharField()

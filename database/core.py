from . import crud
from .models import History, User, db


def create_tables():
    db.create_tables([User, History])


def drop_tables():
    db.drop_tables([User, History])


def connect():
    db.connect()


def get_user_by_user_id(user_id: int) -> User:
    return User.get(User.user_id == user_id)


def get_user_last_queries(user_id: int):
    return crud.read(
        db,
        History,
        join=User,
        filters=[User.user_id == user_id],
        order=History.created_at.asc(),
    )[-5:]

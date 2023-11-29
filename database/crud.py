from typing import Any, Optional, Type

from peewee import Database, Field, Model, ModelSelect


def create(db: Database, model: Type[Model], data: dict[str, Any]) -> None:
    with db.atomic():
        model.create(**data)


def create_many(db: Database, model: Type[Model], data: list[dict[str, Any]]) -> None:
    with db.atomic():
        model.insert_many(data).execute()


def read(
    db: Database,
    model: Type[Model],
    columns: Optional[list[Field]] = None,
    join: Optional[Type[Model]] = None,
    filters: Optional[list[Any]] = None,
    order: Optional[Any] = None,
) -> ModelSelect:
    columns = columns or []
    with db.atomic():
        query = model.select(*columns)
        if join:
            query = query.join(join)

        if filters:
            query = query.where(*filters)

        if order:
            query = query.order_by(order)
        response = query.execute()

    return response


def update(
    db: Database,
    model: Type[Model],
    change: dict,
    filters: Optional[list[Any]] = None,
):
    with db.atomic():
        query = model.update(**change)
        if filters:
            query = query.where(*filters)
        query.execute()


def delete(db: Database, model: Type[Model], filters: list[Any]):
    with db.atomic():
        model.delete().where(*filters)

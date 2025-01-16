import abc

from tinydb import TinyDB
from tinydb.queries import QueryLike
from abc import ABC

from logger import logger
from schemas.base import Base
from settings import settings


class BaseDB(ABC):
    @abc.abstractmethod
    def create(self, instance: Base):
        pass

    @abc.abstractmethod
    def search(self, query):
        pass

    @abc.abstractmethod
    def update(self, query, new_instance: Base):
        pass

    @abc.abstractmethod
    def delete(self, query):
        pass

    @abc.abstractmethod
    def all(self):
        pass


class Tiny(BaseDB):
    def __init__(self, db: TinyDB):
        self.db = db

    def create(self, instance: Base):
        self.db.insert(instance.model_dump())

    def all(self):
        return self.db.all()

    def search(self, query: QueryLike):
        return self.db.search(query)

    def update(self, query: QueryLike, new_instance: Base):
        self.db.update(new_instance.model_dump(), query)

    def delete(self, query: QueryLike):
        self.db.remove(query)


def get_tiny_db():
    try:
        db = TinyDB(settings.db_path)
        return db
    except PermissionError as e:
        logger.error(e)


def get_stats_table(db: TinyDB | None):
    if db is not None:
        return db.table(settings.db_stats_table_name)
    return

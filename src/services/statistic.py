from pydantic import ValidationError
from tinydb import Query
from tinydb.table import Document

from db import BaseDB
from schemas.statistic import StatisticSchema


class StatisticService(object):
    def __init__(self, db: BaseDB):
        self.db = db
        self.stat = Query()

    def _to_pydantic(self, rows: list[Document]) -> list[StatisticSchema]:
        stats_pydantic = []
        for row in rows:
            try:
                stats_pydantic.append(StatisticSchema(**row))
            except ValidationError:
                pass
        return stats_pydantic

    def create(self, instance: StatisticSchema):
        self.db.create(instance)

    def search(self, params: dict) -> list[StatisticSchema]:
        query = self.stat.fragment(params)
        result = self.db.search(query)
        stats_pydantic = self._to_pydantic(result)
        return stats_pydantic

    def all(self) -> list[StatisticSchema]:
        try:
            result = self.db.all()
            stats_pydantic = self._to_pydantic(result)
        except AttributeError:
            stats_pydantic = []
        return stats_pydantic

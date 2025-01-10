from pydantic import ValidationError
from tinydb import Query

from db import BaseDB
from schemas.statistic import StatisticSchema


class StatisticService(object):
    def __init__(self, db: BaseDB):
        self.db = db
        self.stat = Query()

    def create(self, instance: StatisticSchema):
        self.db.create(instance)

    def search(self, params: dict) -> list[StatisticSchema]:
        query = self.stat.fragment(params)
        result = self.db.search(query)
        stats_pydantic = []
        for stat in result:
            try:
                stats_pydantic.append(StatisticSchema(**stat))
            except ValidationError:
                pass
        return stats_pydantic

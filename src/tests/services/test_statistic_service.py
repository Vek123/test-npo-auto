from tests.config import db, stat_service
from schemas.statistic import StatisticSchema


class TestStatisticService:
    def setup_class(self):
        self.valid_statistic = StatisticSchema(
            cpu=10.0,
            ram=[10.0, 20.0],
            rom=[50.0, 100.0],
        )

    def test_stat_create(self):
        stat_service.create(self.valid_statistic)
        response = stat_service.search(self.valid_statistic.model_dump())
        assert len(response) == 1

        stat = response[0]
        assert stat.cpu == self.valid_statistic.cpu
        assert stat.ram == self.valid_statistic.ram
        assert stat.rom == self.valid_statistic.rom

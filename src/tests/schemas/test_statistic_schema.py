from schemas.statistic import StatisticSchema


class TestStatisticSchema:
    def setup_class(self):
        self.valid_statistic = {
            "cpu": 1.0,
            "ram": [10.0, 20.0],
            "rom": [50.0, 100.0],
        }

    def test_schema_create(self):
        schema = StatisticSchema(**self.valid_statistic)
        assert schema.cpu == self.valid_statistic["cpu"]
        assert schema.ram == self.valid_statistic["ram"]
        assert schema.rom == self.valid_statistic["rom"]
from schemas.base import Base


class StatisticSchema(Base):
    cpu: float
    ram: list[float, float]
    rom: list[float, float]

import flet as ft
import pytest

import main
from db import TinyDB, Tiny
from services.statistic import StatisticService


@pytest.fixture(scope="session")
def db(tmp_path_factory):
    temp_path = tmp_path_factory.getbasetemp() / "test.json"
    db = Tiny(TinyDB(temp_path))
    return db


@pytest.fixture(scope="session")
def stat_service(db):
    return StatisticService(db)

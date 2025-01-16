from dependency_injector import containers, providers

from db import Tiny, get_stats_table, get_tiny_db
from services.statistic import StatisticService


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    tiny_db = providers.Factory(
        get_tiny_db,
    )
    tiny_db_table_stats = providers.Factory(
        get_stats_table,
        db=tiny_db
    )
    tiny_db_client = providers.Factory(
        Tiny,
        db=tiny_db_table_stats,
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    gateways = providers.DependenciesContainer()

    stat_service = providers.Factory(
        StatisticService,
        db=gateways.tiny_db_client,
    )


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()

    gateways = providers.Container(
        Gateways,
        config=config,
    )

    services = providers.Container(
        Services,
        config=config,
        gateways=gateways,
    )

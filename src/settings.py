class Settings(object):
    initial_window_size: list[int, int] = [400, 300]
    minimum_window_size: list[int, int] = [300, 200]
    db_path: str = "db.json"
    db_stats_table_name: str = "stats"
    record_active: bool = False
    update_stats_period: float = 1.0


settings = Settings()

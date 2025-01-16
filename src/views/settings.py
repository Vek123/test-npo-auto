import pathlib

import flet as ft
from flet_route import Basket, Params

from settings import settings
from logger import logger


class SettingsView:
    def view(self, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        def save_settings(event: ft.ControlEvent):
            try:
                path = pathlib.Path(setting_db_path.value).resolve()
                if path.exists():
                    settings.db_path = setting_db_path.value
                else:
                    raise FileNotFoundError("DB file not found")
                settings.update_stats_period = max(0.1, float(setting_update_stats_period.value))
            except TypeError:
                error_message.value = "Значение периода некорректно"
                setting_db_path.value = settings.db_path
                logger.debug("Period value is incorrect")
            except FileNotFoundError as e:
                error_message.value = "Файл БД не существует"
                logger.debug(e)
            except Exception:
                error_message.value = "Значения введены некорректно"
                logger.debug("Some written settings values is incorrect")
            else:
                error_message.value = None
            settings.db_stats_table_name = setting_db_stats_table_name.value
            page.update()

        setting_db_path = ft.TextField(
            label="Путь к БД",
            value=settings.db_path,
            border_color=ft.Colors.WHITE,
        )
        setting_db_stats_table_name = ft.TextField(
            label="Название таблицы БД для статистики",
            value=settings.db_stats_table_name,
            border_color=ft.Colors.WHITE,
        )
        setting_update_stats_period = ft.TextField(
            label="Период обновления статистики",
            value=settings.update_stats_period,
            border_color=ft.Colors.WHITE,
        )
        error_message = ft.Text(color=ft.Colors.RED)
        settings_block = ft.Column(
            controls=[
                setting_db_path,
                setting_db_stats_table_name,
                setting_update_stats_period,
                error_message,
            ]
        )
        save_button = ft.FilledButton(
            text="Сохранить",
            on_click=save_settings,
            color=ft.Colors.BLACK,
        )
        return ft.View(
            route="/settings",
            controls=[
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                settings_block,
                                ft.IconButton(
                                    ft.Icons.HOME,
                                    on_click=lambda _: page.go("/")
                                ),
                            ]
                        ),
                        save_button,
                    ]
                ),
            ]
        )

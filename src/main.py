import logging

import flet as ft
from flet_route import path, Routing

from deps.containers import Application
from settings import settings
from views import *
from logger import logger

APP_ROUTES = [
    path("/", view=HomeView().view, clear=True),
    path("/settings", view=SettingsView().view, clear=True),
    path("/history", view=HistoryView().view, clear=True),
]


def main(page: ft.Page):
    page.title = "Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.height = settings.initial_window_size[1]
    page.window.width = settings.initial_window_size[0]
    page.window.min_height = settings.minimum_window_size[1]
    page.window.min_width = settings.minimum_window_size[0]

    Routing(page=page, app_routes=APP_ROUTES)
    page.go(page.route)


if __name__ == "__main__":
    application = Application()
    application.wire(packages=["views"])
    try:
        ft.app(main)
    except RuntimeError as e:
        logger.info(e)

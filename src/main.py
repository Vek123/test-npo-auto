import flet as ft
from flet_route import path, Routing

from deps.containers import Application
from settings import settings
from views import *


def main(page: ft.Page):
    page.title = "Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.height = settings.initial_window_size[1]
    page.window.width = settings.initial_window_size[0]
    page.window.min_height = settings.minimum_window_size[1]
    page.window.min_width = settings.minimum_window_size[0]

    app_routes = [
        path("/", view=Home().view, clear=True),
        path("/settings", view=Settings().view, clear=True),
        path("/history", view=History().view, clear=True),
    ]
    Routing(page=page, app_routes=app_routes)
    page.go(page.route)


application = Application()
application.wire(packages=["views"])
try:
    ft.app(main)
except RuntimeError:
    pass

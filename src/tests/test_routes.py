from flet_route import path
from unittest import TestCase

from main import APP_ROUTES
from views import HomeView, HistoryView, SettingsView


class TestRoutes(TestCase):
    def setUp(self):
        self.valid_routes = [
            tuple(path("/", view=HomeView().view, clear=True)),
            tuple(path("/settings", view=SettingsView().view, clear=True)),
            tuple(path("/history", view=HistoryView().view, clear=True)),
        ]

    def test_routes(self):
        valid_routes_count = 0
        for idx, route in enumerate(APP_ROUTES):
            if (route[0] == self.valid_routes[idx][0]
                    and route[1] == self.valid_routes[idx][1]
                    and route[2].__dict__.get("__wrapped__") == HomeView.view):
                valid_routes_count += 1
            else:
                assert f"Route {route} is not valid."
        assert (valid_routes_count == len(self.valid_routes),
                "Some route does not exist.")

from typing import Any

import flet as ft


def create_filled_button(params: dict[str, Any] | None = None, *args, **kwargs) -> ft.FilledButton:
    if not params:
        params = dict()
    button = ft.FilledButton(**kwargs)
    for key, val in params.items():
        setattr(button, key, val)
    return button

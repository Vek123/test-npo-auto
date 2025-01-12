import threading
import time
from typing import Any

import flet as ft
import psutil
from dependency_injector.wiring import Provide, inject
from flet_route import Params, Basket

from services.statistic import StatisticService
from settings import settings
from schemas.statistic import StatisticSchema
from deps.containers import Application
from utils import create_filled_button


timer_mutex = threading.Lock()


class Home:
    cpu_load_template: str = "ЦП: %.2f %%"
    ram_template: str = "ОЗУ: %.2f / %.2f МБ"
    rom_template: str = "ПЗУ: %.2f / %.2f ГБ"
    stats_font_size: int = 20
    record_button_settings: tuple[dict[str, Any]] = (
        {
            "text": "Начать запись",
            "bgcolor": ft.Colors.RED_ACCENT_700,
            "color": ft.Colors.WHITE,
        },
        {
            "text": "Остановить запись",
            "bgcolor": ft.Colors.RED_ACCENT_200,
            "color": ft.Colors.WHITE,
        },
    )
    timer_seconds: int = 0

    @inject
    def view(
            self,
            page: ft.Page,
            params: Params,
            basket: Basket,
            stat_service: StatisticService = Provide[Application.services.stat_service],
    ) -> ft.View:
        def toggle_record(event: ft.ControlEvent):
            settings.record_active = not settings.record_active
            if settings.record_active:
                timer.visible = True
                threading.Thread(target=activate_timer, daemon=True).start()
            else:
                self.timer_seconds = 0
                timer.visible = False
            for key, val in self.record_button_settings[settings.record_active].items():
                setattr(event.control, key, val)
            page.update()

        for variant in self.record_button_settings:
            variant["on_click"] = toggle_record

        def save_stat(stat: StatisticSchema, ):
            stat_service.create(stat)

        def get_size(bts: float, to: str) -> float:
            size = 1024
            for item in ["", "K", "M", "G", "T", "P"]:
                if item == to:
                    return bts
                bts /= size

        def activate_timer():
            while page.route == "/" and settings.record_active:
                timer_mutex.acquire()
                seconds = self.timer_seconds % 60
                minutes = self.timer_seconds // 60
                make_timer_value(timer, minutes, seconds)
                self.timer_seconds += 1
                timer_mutex.release()
                page.update(timer)
                time.sleep(1)

        def make_timer_value(timer: ft.Text, minutes: int, seconds: int):
            timer.value = (f"{"0" if minutes < 10 else ""}"
                           f"{minutes}:"
                           f"{"0" if seconds < 10 else ""}"
                           f"{seconds}")

        def update_stats():
            while page.route == "/":
                try:
                    cpu_load = psutil.cpu_percent()
                    ram_total = get_size(psutil.virtual_memory().total, "M")
                    ram_used = get_size(psutil.virtual_memory().used, "M")
                    disks = psutil.disk_partitions()
                    rom_used_total = [0.0, 0.0]
                    for disk in disks:
                        try:
                            usage = psutil.disk_usage(disk.mountpoint)
                        except PermissionError:
                            continue
                        rom_used_total[0] += usage.used
                        rom_used_total[1] += usage.total
                    rom_used_total[0] = get_size(rom_used_total[0], "G")
                    rom_used_total[1] = get_size(rom_used_total[1], "G")

                    cpu.value = self.cpu_load_template % cpu_load
                    ram.value = self.ram_template % (ram_used, ram_total)
                    rom.value = self.rom_template % (
                        rom_used_total[0], rom_used_total[1]
                    )

                    if settings.record_active:
                        save_stat(
                            StatisticSchema(
                                cpu=cpu_load,
                                ram=[ram_used, ram_total],
                                rom=rom_used_total,
                            )
                        )

                    page.update(cpu, ram, rom)
                    time.sleep(settings.update_stats_period)
                except Exception:
                    time.sleep(5)

        cpu = ft.Text(self.cpu_load_template % 0.0, size=self.stats_font_size)
        ram = ft.Text(self.ram_template % (0.0, 0.0), size=self.stats_font_size)
        rom = ft.Text(self.rom_template % (0.0, 0.0), size=self.stats_font_size)

        stats = ft.Column(controls=[
            ft.Text("Уровень загруженности"),
            cpu,
            ram,
            rom,
        ])
        record_button = create_filled_button(
            self.record_button_settings[settings.record_active]
        )
        timer = ft.Text("00:00", visible=False)

        threading.Thread(target=update_stats, daemon=True).start()
        if settings.record_active:
            timer.visible = True
            threading.Thread(target=activate_timer, daemon=True).start()

        return ft.View(
            route="/",
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
                                stats,
                                ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.IconButton(
                                            ft.Icons.SETTINGS,
                                            on_click=lambda _: page.go("/settings"),
                                        ),
                                        ft.IconButton(
                                            ft.Icons.HISTORY,
                                            on_click=lambda _: page.go("/history"),
                                        )
                                    ]
                                ),
                            ],
                        ),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                record_button,
                                timer,
                            ],
                        ),
                    ],
                ),
            ]
        )

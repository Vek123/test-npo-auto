import flet as ft
from flet_route import Params, Basket
from dependency_injector.wiring import Provide, inject

from deps.containers import Application
from schemas.statistic import StatisticSchema
from services.statistic import StatisticService


class History:
    @inject
    def view(
            self,
            page: ft.Page,
            params: Params,
            basket: Basket,
            stat_service: StatisticService = Provide[Application.services.stat_service],
    ) -> ft.View:
        stats = stat_service.all()
        stats_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("CPU Load, %")),
                ft.DataColumn(ft.Text("RAM Usage, МБ")),
                ft.DataColumn(ft.Text("RAM All, МБ")),
                ft.DataColumn(ft.Text("ROM Usage, ГБ")),
                ft.DataColumn(ft.Text("ROM All, ГБ")),
            ],
            rows=[
                ft.DataRow([
                    ft.DataCell(ft.Text(f"{row.cpu}")),
                    ft.DataCell(ft.Text(f"{round(row.ram[0], 2)}")),
                    ft.DataCell(ft.Text(f"{round(row.ram[1], 2)}")),
                    ft.DataCell(ft.Text(f"{round(row.rom[0], 2)}")),
                    ft.DataCell(ft.Text(f"{round(row.rom[1], 2)}")),
                ]) for row in stats
            ],
        )

        return ft.View(
            scroll=ft.ScrollMode.ALWAYS,
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
                                stats_table,
                                ft.IconButton(
                                    ft.Icons.HOME,
                                    on_click=lambda _: page.go("/")
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )

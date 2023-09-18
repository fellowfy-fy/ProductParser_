import logging
import os
from dataclasses import dataclass
from datetime import date
from parser.models import ParseTask
from time import time

from django.conf import settings
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from accounts.models import CustomUser
from products.models import Product


@dataclass
class ReportParams:
    user: CustomUser

    filter_task: ParseTask | None = None
    date_from: date | None = None
    date_to: date | None = None
    filter_product: Product | None = None  # Filter data by product


class BaseExcelExport:
    name = "base"  # Report name
    params: ReportParams
    book: Workbook
    sheet: Worksheet
    log: logging.Logger

    row_index: int = 0
    color_green = "FF00FF00"
    color_red = "FFFF0000"

    def __init__(self, params: ReportParams, log_level=logging.INFO) -> None:
        self.params = params
        self.log = logging.getLogger("Excel-" + self.name)
        self.log.setLevel(log_level)

    def get_workbook(self) -> Workbook:
        workbook = Workbook()
        return workbook

    def get_report_path(self, mkdir: bool = True) -> str:
        """Get report result path"""
        path = os.path.join(settings.MEDIA_ROOT, f"reports/{self.name}.xlsx")
        if mkdir:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    def sheet_init(self) -> None:
        """Init excel worksheet"""
        self.book = self.get_workbook()
        # self.sheet = self.book.create_sheet("Отчет")
        self.sheet = self.book.active

    def sheet_process(self) -> None:
        """Add data to excel worksheet"""
        raise NotImplementedError()

    def sheet_save(self) -> str:
        """Save excel worksheet"""
        report_path = self.get_report_path()
        self.book.save(report_path)
        return report_path

    def export(self) -> str:
        """Run export"""
        self.log.info(f"Starting excel export {self.name}...")

        started = time()
        self.sheet_init()
        self.sheet_process()

        self.log.info(f"Saving excel export {self.name}...")
        report_path = self.sheet_save()

        finished = time()
        time_left = round(finished - started, 2)
        self.log.info(f"Finished excel export {self.name} by {time_left} secs. Report path: {report_path}.")
        return report_path

    def insert_row(self, values: list[str]) -> None:
        self.sheet.append(values)

    def insert_headers(self, values: list[str]) -> None:
        self.insert_row(values)

    def last_row_colors(self, colors: list[str | None]) -> None:
        row = self.sheet.max_row
        for col_idx, color in enumerate(colors, start=1):
            if not color:
                continue
            cell = self.sheet.cell(row, col_idx)

            # cell.style.font.color.index = color
            cell.font = Font(color=color)

    # def _get_template_path(self):
    #     return os.path.join(os.path.dirname(__file__), "excel_templates", f"report_{self.name}.xlsx")

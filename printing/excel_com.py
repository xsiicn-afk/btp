from pathlib import Path

import pythoncom
import win32com.client

from printing.address_writer import AddressWriter
from printing.qr_writer import QrWriter
from printing.specification_writer import SpecificationWriter


class ExcelCom:

    def __init__(self):

        self.excel = None
        self.workbook = None

    # ---------------------------------------------------------

    def open(self, filename: str):

        pythoncom.CoInitialize()

        self.excel = win32com.client.DispatchEx(
            "Excel.Application"
        )

        self.excel.Visible = False
        self.excel.DisplayAlerts = False

        self.workbook = self.excel.Workbooks.Open(
            str(Path(filename).resolve())
        )

    # ---------------------------------------------------------

    def close(self):

        try:

            if self.workbook is not None:
                self.workbook.Close(False)

        finally:

            if self.excel is not None:
                self.excel.Quit()

            pythoncom.CoUninitialize()

    # ---------------------------------------------------------

    def sheet(self, name: str):

        return self.workbook.Worksheets(name)

    # ---------------------------------------------------------

    def specification_sheet(self):

        sheet = self.sheet("Спецификация")

        sheet.Activate()

        return sheet

    # ---------------------------------------------------------

    def save_as(self, filename: str):

        self.workbook.SaveAs(
            str(Path(filename).resolve())
        )

    # ---------------------------------------------------------

    def prepare_for_print(
        self,
        page_layout,
    ):

        page = self.specification_sheet().PageSetup

        page.PrintArea = "$A$1:$BJ$52"

        page.Zoom = False

        page.FitToPagesWide = 1
        page.FitToPagesTall = 1

        page.Orientation = 2

        page.LeftMargin = 0
        page.RightMargin = 0
        page.TopMargin = 0
        page.BottomMargin = 0

    # ---------------------------------------------------------

    def export_pdf(
        self,
        label,
        filename,
    ):

        self.prepare_for_print(
            label.layout
        )

        self.specification_sheet().ExportAsFixedFormat(
            0,
            str(Path(filename).resolve()),
        )

    # ---------------------------------------------------------

    def print(
        self,
        label,
    ):

        self.prepare_for_print(
            label.layout
        )

        self.specification_sheet().PrintOut()

    # ---------------------------------------------------------

    def write(
        self,
        sheet_name,
        cell,
        value,
    ):

        self.sheet(sheet_name).Range(
            cell
        ).Value = value

    # ---------------------------------------------------------

    def set_formula(
        self,
        sheet_name,
        cell,
        formula,
    ):

        self.sheet(sheet_name).Range(
            cell
        ).Formula = formula

    # ---------------------------------------------------------

    def write_specification(
        self,
        label,
        block="TOP_LEFT",
    ):

        SpecificationWriter(
            self.specification_sheet(),
            block,
        ).write(label)

    # ---------------------------------------------------------

    def write_addresses(
        self,
        label,
    ):

        AddressWriter(
            self.specification_sheet()
        ).write(label)

    # ---------------------------------------------------------

    def insert_serial_qr(
        self,
        filename,
        block="TOP_LEFT",
    ):

        QrWriter(
            self.specification_sheet(),
            block,
        ).serial(
            filename
        )

    # ---------------------------------------------------------

    def insert_article_qr(
        self,
        filename,
        block="TOP_LEFT",
    ):

        QrWriter(
            self.specification_sheet(),
            block,
        ).article(
            filename
        )
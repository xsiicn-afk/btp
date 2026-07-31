from pathlib import Path

import pythoncom
import win32com.client


class ExcelCom:
    """
    Тонкая обёртка над Microsoft Excel COM.
    Отвечает только за работу с Excel.
    """

    def __init__(self):

        self.excel = None
        self.workbook = None

    # ---------------------------------------------------------

    def open(
        self,
        filename: str,
    ):

        pythoncom.CoInitialize()

        self.excel = win32com.client.DispatchEx(
            "Excel.Application"
        )

        self.excel.Visible = False
        self.excel.DisplayAlerts = False

        self.workbook = self.excel.Workbooks.Open(
            str(
                Path(filename).resolve()
            )
        )

    # ---------------------------------------------------------

    def close(self):

        try:

            if self.workbook is not None:

                self.workbook.Close(False)

        finally:

            if self.excel is not None:

                self.excel.Quit()

            self.workbook = None
            self.excel = None

            pythoncom.CoUninitialize()

    # ---------------------------------------------------------

    def sheet(
        self,
        name: str,
    ):

        return self.workbook.Worksheets(name)
        # ---------------------------------------------------------

    def specification_sheet(self):

        sheet = self.sheet(
            "Спецификация"
        )

        sheet.Activate()

        return sheet

    # ---------------------------------------------------------

    def passport_sheet(self):

        sheet = self.sheet(
            "Паспорт"
        )

        sheet.Activate()

        return sheet

    # ---------------------------------------------------------

    def sticker_sheet(self):

        sheet = self.sheet(
            "Адрес"
        )

        sheet.Activate()

        return sheet

    
    # ---------------------------------------------------------

    def save_as(
        self,
        filename: str,
    ):

        self.workbook.SaveAs(
            str(
                Path(filename).resolve()
            )
        )

    # ---------------------------------------------------------
     
    def prepare_for_print(
        self,
        sheet,
        print_area: str | None = None,
    ):
        """
        Подготавливает лист к печати.

        Если указана область печати —
        используется только она.
        Иначе печатается весь лист.
        """

        page = sheet.PageSetup

        if print_area:

            page.PrintArea = print_area

        else:

            page.PrintArea = ""

        page.Zoom = False
        page.FitToPagesWide = 1
        page.FitToPagesTall = 1

        page.LeftMargin = 0
        page.RightMargin = 0
        page.TopMargin = 0
        page.BottomMargin = 0
    
    # ---------------------------------------------------------

    def clear_range(
        self,
        sheet,
        range_address: str,
    ):
        """
        Полностью очищает диапазон
        вместе с изображениями.
        """

        rng = sheet.Range(
            range_address
        )

        for shape in list(sheet.Shapes):

            try:

                cell = shape.TopLeftCell

                if (
                    cell.Row >= rng.Row
                    and cell.Row < rng.Row + rng.Rows.Count
                    and cell.Column >= rng.Column
                    and cell.Column < rng.Column + rng.Columns.Count
                ):

                    shape.Delete()

            except Exception:

                pass

        rng.Clear()     

    # ---------------------------------------------------------

    def export_pdf(
        self,
        sheet,
        filename: str,
        print_area: str | None = None,
    ):
        """
        Экспортирует выбранный лист в PDF.

        При необходимости ограничивает
        область печати.
        """

        self.prepare_for_print(
            sheet,
            print_area,
        )

        sheet.ExportAsFixedFormat(
            0,
            str(
                Path(filename).resolve()
            ),
        )
    # ---------------------------------------------------------

    def print(
        self,
        sheet,
        print_area: str | None = None,
    ):
        """
        Печатает выбранный лист.

        Если указана область печати —
        печатается только она.
        """

        self.prepare_for_print(
            sheet,
            print_area,
        )

        sheet.PrintOut()

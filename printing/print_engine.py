import tempfile
from pathlib import Path

from models.label_model import LabelModel

from printing.excel_specification import ExcelSpecification
from printing.excel_passport import ExcelPassport
from printing.bartender_sticker import BarTenderSticker

from services.settings_service import SettingsService


class PrintEngine:
    """
    Движок печати.

    Новая схема:
        одно изделие → одна спецификация 100×150.
    """

    def __init__(self):

        self.settings = SettingsService()

        self.specification = ExcelSpecification()

        self.passport = ExcelPassport()

        self.sticker = BarTenderSticker(
            bartender=(
                r"C:\Program Files\Seagull"
                r"\BarTender 2021"
                r"\BarTend.exe"
            ),
        )

    # ---------------------------------------------------------

    def export_excel(
        self,
        label: LabelModel,
        filename: str,
    ):

        self.specification.build(
            label,
            filename,
        )

    # ---------------------------------------------------------

    def export_pdf(
        self,
        label: LabelModel,
        filename: str,
    ):

        self.specification.export_pdf(
            label,
            filename,
        )

    # ---------------------------------------------------------

    def export_passport_excel(
        self,
        label: LabelModel,
        filename: str,
    ):

        self.passport.build(
            label,
            filename,
        )

    # ---------------------------------------------------------

    def export_passport_pdf(
        self,
        label: LabelModel,
        filename: str,
    ):

        self.passport.export_pdf(
            label,
            filename,
        )
    # ---------------------------------------------------------

    def print_to_printer(
        self,
        label: LabelModel,
    ):

        printer = self.settings.get_spec_printer()

        self.specification.print_document(
            label,
            printer_name=printer,
        )

    # ---------------------------------------------------------

    def print_passport(
        self,
        label: LabelModel,
    ):

        printer = self.settings.get_passport_printer()

        self.passport.print_document(
            label,
            printer_name=printer,
        )

    # ---------------------------------------------------------

    def print_sticker(
        self,
        label: LabelModel,
    ):

        printer = self.settings.get_sticker_printer()

        return self.sticker.print(
            label,
            printer_name=printer,
        )

    # ---------------------------------------------------------

    def close(self):

        self.sticker.close()

    # ---------------------------------------------------------

    def build_temp_excel(
        self,
        label: LabelModel,
    ) -> Path:

        temp_dir = (
            Path(tempfile.gettempdir())
            / "ByTop"
        )

        temp_dir.mkdir(exist_ok=True)

        filename = (
            temp_dir
            / "Specification.xlsx"
        )

        self.export_excel(
            label,
            str(filename),
        )

        return filename
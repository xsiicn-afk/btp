import os
import tempfile
from pathlib import Path

from models.label_model import LabelModel

from printing.excel_specification import ExcelSpecification
from services.settings_service import SettingsService


class PrintEngine:
    """
    Движок формирования документов.

    Excel используется только для генерации.
    Печать выполняется стандартной программой
    просмотра PDF.
    """

    def __init__(self):

        self.settings = SettingsService()

        template = self.settings.get(
            "template_path"
        )

        self.excel = ExcelSpecification(
            template
        )

    # ---------------------------------------------------------

    def export_pdf(
        self,
        label: LabelModel,
        filename: str,
    ):

        self.excel.export_pdf(
            label,
            filename,
        )

    # ---------------------------------------------------------

    def export_excel(
        self,
        label: LabelModel,
        filename: str,
    ):

        self.excel.build(
            label,
            filename,
        )

    # ---------------------------------------------------------

    def print_to_printer(
        self,
        label: LabelModel,
    ):
        """
        Создает временный PDF и открывает его
        стандартной программой Windows.

        Дальнейшая печать выполняется самим
        пользователем через привычный диалог.
        """

        temp_dir = Path(
            tempfile.gettempdir()
        ) / "ByTop"

        temp_dir.mkdir(
            exist_ok=True
        )

        pdf_file = (
            temp_dir /
            f"SN{label.serial}.pdf"
        )

        self.export_pdf(
            label,
            str(pdf_file),
        )

        os.startfile(
            str(pdf_file)
        )
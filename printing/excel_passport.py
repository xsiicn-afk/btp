from pathlib import Path

from models.label_model import LabelModel

from printing.excel_com import ExcelCom
from printing.excel_passport_writer import (
    ExcelPassportWriter,
)
from printing.printer_utils import (
    temporary_default_printer,
)
from services.template_service import TemplateService


class ExcelPassport:
    """
    Формирование паспорта изделия.

    Один LabelModel = один лист.

    Шаблон автоматически берётся
    из выбранного профиля шаблонов.
    """

    def __init__(
        self,
        template: str | None = None,
    ):

        if not template:
            template = TemplateService().passport()

        self.template = Path(template)

        if not self.template.exists():

            profile = (
                TemplateService()
                .current_profile()
            )

            raise FileNotFoundError(
                "В профиле шаблонов "
                f'"{profile}" отсутствует файл '
                f"{self.template.name}"
            )

    # ---------------------------------------------------------

    @staticmethod
    def coordinates() -> dict[str, str]:

        return {

            "TITLE": "B3",

            "DATE": "B32",

            "SERIAL": "H5",

            "ARTICLE": "H6",

            "MODEL": "H7",

        }

    # ---------------------------------------------------------

    def fill_passport(
        self,
        excel: ExcelCom,
        label: LabelModel,
    ):

        sheet = excel.passport_sheet()

        writer = ExcelPassportWriter(
            sheet,
            self.coordinates(),
        )

        writer.write(
            label
        )

    # ---------------------------------------------------------

    def build(
        self,
        label: LabelModel,
        output_file: str,
    ):

        excel = ExcelCom()

        excel.open(
            str(self.template)
        )

        try:

            self.fill_passport(
                excel,
                label,
            )

            excel.save_as(
                output_file,
            )

        finally:

            excel.close()

    # ---------------------------------------------------------

    def export_pdf(
        self,
        label: LabelModel,
        pdf_file: str,
    ):

        excel = ExcelCom()

        excel.open(
            str(self.template)
        )

        try:

            self.fill_passport(
                excel,
                label,
            )

            sheet = excel.passport_sheet()

            excel.export_pdf(
                sheet,
                pdf_file,
            )

        finally:

            excel.close()

    # ---------------------------------------------------------

    def print_document(
        self,
        label: LabelModel,
        printer_name: str | None = None,
    ):

        with temporary_default_printer(
            printer_name
        ):

            excel = ExcelCom()

            excel.open(
                str(self.template)
            )

            try:

                self.fill_passport(
                    excel,
                    label,
                )

                sheet = (
                    excel.passport_sheet()
                )

                excel.print(
                    sheet,
                )

            finally:

                excel.close()
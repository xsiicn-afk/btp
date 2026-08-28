from pathlib import Path
import tempfile

from openpyxl import load_workbook

from models.label_model import LabelModel
from printing.specification_writer import SpecificationWriter
from services.template_service import TemplateService


class ExcelSpecification:
    """
    Спецификация 100×150.

    Один LabelModel = одна этикетка.
    """

    def __init__(self, template: str | None = None):

        if not template:
            template = TemplateService().spec()

        self.template = Path(template)

        if not self.template.exists():

            profile = TemplateService().current_profile()

            raise FileNotFoundError(
                f'В профиле "{profile}" отсутствует {self.template.name}'
            )

    # ---------------------------------------------------------

    def build(
        self,
        label: LabelModel,
        output_file: str,
    ):

        workbook = load_workbook(self.template)

        sheet = workbook.active

        SpecificationWriter(sheet).write(label)

        workbook.save(output_file)

    # ---------------------------------------------------------

    def export_pdf(
        self,
        label: LabelModel,
        pdf_file: str,
    ):

        temp = (
            Path(tempfile.gettempdir())
            / "ByTop"
        )

        temp.mkdir(exist_ok=True)

        xlsx = temp / "Specification.xlsx"

        self.build(label, str(xlsx))

        from printing.excel_com import ExcelCom

        excel = ExcelCom()

        excel.open(str(xlsx))

        try:

            excel.export_pdf(
                excel.workbook.ActiveSheet,
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

        temp = (
            Path(tempfile.gettempdir())
            / "ByTop"
        )

        temp.mkdir(exist_ok=True)

        xlsx = temp / "Specification.xlsx"

        self.build(label, str(xlsx))

        from printing.excel_com import ExcelCom
        from printing.printer_utils import temporary_default_printer

        with temporary_default_printer(printer_name):

            excel = ExcelCom()

            excel.open(str(xlsx))

            try:

                sheet = excel.workbook.ActiveSheet

                excel.print(sheet)

            finally:

                excel.close()
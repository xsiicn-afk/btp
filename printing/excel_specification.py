from pathlib import Path

from models.label_model import LabelModel
from models.page_layout import PageLayout

from printing.excel_com import ExcelCom
from services.qr_service import QrService


class ExcelSpecification:
    """
    Формирование производственной спецификации.
    """

    def __init__(self, template: str):

        self.template = Path(template)

        if not self.template.exists():
            raise FileNotFoundError(
                f"Не найден шаблон {self.template}"
            )

        self.qr = QrService()

    # ---------------------------------------------------------

    def blocks(self, layout):

        if layout == PageLayout.ONE_SPEC_THREE_ADDRESS:
            return ["TOP_LEFT"]

        if layout == PageLayout.TWO_SPEC_TWO_ADDRESS:
            return [
                "TOP_LEFT",
                "TOP_RIGHT",
            ]

        if layout == PageLayout.THREE_SPEC_ONE_ADDRESS:
            return [
                "TOP_LEFT",
                "TOP_RIGHT",
                "BOTTOM_LEFT",
            ]

        return [
            "TOP_LEFT",
            "TOP_RIGHT",
            "BOTTOM_LEFT",
            "BOTTOM_RIGHT",
        ]

    # ---------------------------------------------------------

    def fill_document(
        self,
        excel,
        label,
    ):

        serial_qr = self.qr.create_serial(
            label.serial
        )

        article_qr = self.qr.create_article(
            label.article_code
        )

        for block in self.blocks(label.layout):

            excel.write_specification(
                label,
                block,
            )

            excel.insert_serial_qr(
                serial_qr,
                block,
            )

            excel.insert_article_qr(
                article_qr,
                block,
            )

        excel.write_addresses(label)

    # ---------------------------------------------------------

    def build(
        self,
        label: LabelModel,
        output_file: str,
    ):

        excel = ExcelCom()

        excel.open(str(self.template))

        try:

            self.fill_document(
                excel,
                label,
            )

            excel.save_as(
                output_file
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

        excel.open(str(self.template))

        try:

            self.fill_document(
                excel,
                label,
            )

            excel.export_pdf(
                label,
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

        excel = ExcelCom()

        excel.open(str(self.template))

        try:

            self.fill_document(
                excel,
                label,
            )

            if printer_name:

                try:
                    excel.excel.ActivePrinter = printer_name

                except Exception as e:

                    print(
                        "PRINTER =",
                        printer_name,
                    )

                    print(
                        "ERROR =",
                        e,
                    )

            excel.print(label)

        finally:

            excel.close()
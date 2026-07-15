from pathlib import Path

from models.label_model import LabelModel

from printing.excel_com import ExcelCom
from services.qr_service import QrService


class ExcelSpecification:
    """
    Формирование производственной спецификации.
    """

    def __init__(
        self,
        template: str,
    ):

        self.template = Path(template)

        if not self.template.exists():

            raise FileNotFoundError(
                f"Не найден шаблон {self.template}"
            )

        self.qr = QrService()

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

            
            excel.write_specification(label)
            excel.write_addresses(label)

            #
            # QR серийного номера
            #

            serial_qr = self.qr.create_serial(
                label.serial
            )

            excel.insert_serial_qr(
                serial_qr
            )

            #
            # QR артикула
            #

            article_qr = self.qr.create_article(
                label.article_code
            )

            excel.insert_article_qr(
                article_qr
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

        excel.open(
            str(self.template)
        )

        try:

            
            excel.write_specification(label)
            excel.write_addresses(label)
            
            serial_qr = self.qr.create_serial(
                label.serial
            )

            excel.insert_serial_qr(
                serial_qr
            )

            article_qr = self.qr.create_article(
                label.article_code
            )

            excel.insert_article_qr(
                article_qr
            )
            excel.export_pdf(
                label,
                pdf_file
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

        excel.open(
            str(self.template)
        )

        try:

            #
            # Заполняем шаблон
            #

            
            excel.write_specification(label)
            excel.write_addresses(label)
            #
            # QR серийного номера
            #

            serial_qr = self.qr.create_serial(
                label.serial
            )

            excel.insert_serial_qr(
                serial_qr
            )

            #
            # QR артикула
            #

            article_qr = self.qr.create_article(
                label.article_code
            )

            excel.insert_article_qr(
                article_qr
            )

            #
            # Если выбран конкретный принтер
            #

            if printer_name:

                try:

                    excel.excel.ActivePrinter = printer_name

                except Exception as e:

                    print("PRINTER =", printer_name)
                    print("ERROR =", e)

                raise

            excel.print(label)

        finally:

            excel.close()
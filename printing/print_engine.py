import tempfile
from pathlib import Path

from models.label_model import LabelModel
from printing.excel_specification import ExcelSpecification
from printing.excel_passport import ExcelPassport
from printing.bartender_sticker import BarTenderSticker
from services.settings_service import SettingsService


class PrintEngine:
    """
    Движок формирования и печати
    производственных документов.
    """

    TOTAL_POSITIONS = 4

    def __init__(self):

        self.settings = SettingsService()

        template = self.settings.get(
            "template_path"
        )

        passport_template = self.settings.get(
            "passport_template_path"
        )

        self.specification = ExcelSpecification(
            template
        )

        self.passport = ExcelPassport(
            passport_template
        )

        self.sticker = BarTenderSticker(
            template=(
                r"C:\Intel\project"
                r"\resources\templates"
                r"\sticker.btw"
            ),
            bartender=(
                r"C:\Program Files\Seagull"
                r"\BarTender 2021"
                r"\BarTend.exe"
            ),
        )

    # ---------------------------------------------------------

    @staticmethod
    def available_positions(
        start_position: int = 1,
    ) -> list[int]:
        """
        Возвращает список свободных позиций
        начиная с указанной.

        1 -> [1, 2, 3, 4]
        2 -> [2, 3, 4]
        3 -> [3, 4]
        4 -> [4]
        """

        start_position = max(
            1,
            min(
                start_position,
                PrintEngine.TOTAL_POSITIONS,
            ),
        )

        return list(
            range(
                start_position,
                PrintEngine.TOTAL_POSITIONS + 1,
            )
        )

    # ---------------------------------------------------------

    @classmethod
    def pages_required(
        cls,
        labels_count: int,
        first_position: int = 1,
    ) -> int:
        """
        Возвращает количество листов,
        необходимых для печати указанного
        количества спецификаций.
        """

        if labels_count <= 0:
            return 0

        first_capacity = len(
            cls.available_positions(
                first_position
            )
        )

        if labels_count <= first_capacity:
            return 1

        labels_count -= first_capacity

        full_pages = (
            labels_count
            // cls.TOTAL_POSITIONS
        )

        if (
            labels_count
            % cls.TOTAL_POSITIONS
        ):
            full_pages += 1

        return 1 + full_pages

    # ---------------------------------------------------------

    @classmethod
    def paginate(
        cls,
        labels: list[LabelModel],
        first_position: int = 1,
    ) -> list[
        tuple[
            list[LabelModel],
            list[int],
        ]
    ]:
        """
        Разбивает список этикеток
        на страницы.
        """

        pages = []

        current_start = first_position
        index = 0

        while index < len(labels):

            positions = (
                cls.available_positions(
                    current_start
                )
            )

            capacity = len(
                positions
            )

            page_labels = labels[
                index:index + capacity
            ]

            page_positions = positions[
                :len(page_labels)
            ]

            pages.append(
                (
                    page_labels,
                    page_positions,
                )
            )

            index += len(
                page_labels
            )

            current_start = 1

        return pages

    # ---------------------------------------------------------

    def export_excel(
        self,
        labels: list[LabelModel],
        filename: str,
        first_position: int = 1,
    ):

        for page_number, (
            page_labels,
            positions,
        ) in enumerate(
            self.paginate(
                labels,
                first_position,
            )
        ):

            if page_number == 0:

                self.specification.build(
                    page_labels,
                    filename,
                    positions,
                )

    # ---------------------------------------------------------

    def export_pdf(
        self,
        labels: list[LabelModel],
        filename: str,
        first_position: int = 1,
    ):

        for page_number, (
            page_labels,
            positions,
        ) in enumerate(
            self.paginate(
                labels,
                first_position,
            )
        ):

            if page_number == 0:

                self.specification.export_pdf(
                    page_labels,
                    filename,
                    positions,
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
        labels: list[LabelModel],
        first_position: int = 1,
    ):

        printer = self.settings.get(
            "printer"
        )

        for (
            page_labels,
            positions,
        ) in self.paginate(
            labels,
            first_position,
        ):

            self.specification.print_document(
                page_labels,
                positions,
                printer_name=printer,
            )

    # ---------------------------------------------------------

    def print_passport(
        self,
        label: LabelModel,
    ):

        printer = self.settings.get(
            "printer"
        )

        self.passport.print_document(
            label,
            printer_name=printer,
        )

    # ---------------------------------------------------------

    def print_sticker(
        self,
        label: LabelModel,
    ):

        return self.sticker.print(
            label
        )

    # ---------------------------------------------------------

    def close(self):

        self.sticker.close()

    # ---------------------------------------------------------

    def build_temp_excel(
        self,
        labels: list[LabelModel],
        first_position: int = 1,
    ) -> Path:

        temp_dir = (
            Path(
                tempfile.gettempdir()
            )
            / "ByTop"
        )

        temp_dir.mkdir(
            exist_ok=True,
        )

        filename = (
            temp_dir
            / "Specification.xlsx"
        )

        self.export_excel(
            labels,
            str(filename),
            first_position,
        )

        return filename
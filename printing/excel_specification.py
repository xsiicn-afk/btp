from pathlib import Path

from models.label_model import LabelModel

from printing.excel_com import ExcelCom
from printing.layout_coordinates import (
    get_layout,
    get_print_area,
)
from printing.specification_writer import (
    SpecificationWriter,
)
from printing.printer_utils import (
    temporary_default_printer,
)


class ExcelSpecification:
    """
    Формирование страницы спецификации.

    Страница может содержать
    от одной до четырёх спецификаций.

    Каждая спецификация располагается
    в одной из позиций листа.
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

    # ---------------------------------------------------------

    def fill_page(
        self,
        excel: ExcelCom,
        labels: list[LabelModel],
        positions: list[int],
    ):

        if len(labels) != len(positions):

            raise ValueError(
                "Количество позиций не совпадает "
                "с количеством спецификаций."
            )

        sheet = excel.specification_sheet()

        for label, position in zip(
            labels,
            positions,
        ):

            coords = get_layout(
                position
            )

            writer = SpecificationWriter(
                sheet,
                coords,
            )

            writer.write(
                label
            )

    # ---------------------------------------------------------

    @staticmethod
    def print_area(
        positions: list[int],
    ) -> str:
        """
        Область для экспорта.

        Для PDF можно использовать область,
        соответствующую выбранным позициям.
        """

        return get_print_area(
            positions
        )

    # ---------------------------------------------------------

    @staticmethod
    def full_print_area() -> str:
        """
        Полная область листа спецификации.

        ВАЖНО:

        При печати на физический лист всегда
        печатается полный макет 2 x 2.

        Неиспользуемые блоки предварительно
        очищаются методом clear_unused_blocks().

        Благодаря этому выбранная позиция
        сохраняет своё физическое место:

            1 | 2
            -----
            3 | 4
        """

        return "A1:BG53"

    # ---------------------------------------------------------

    @staticmethod
    def clear_unused_blocks(
        excel: ExcelCom,
        positions: list[int],
    ):
        """
        Удаляет неиспользуемые блоки
        перед печатью.

        Книга после печати закрывается
        без сохранения.
        """

        used = set(
            positions
        )

        sheet = (
            excel.specification_sheet()
        )

        blocks = {
            1: "A1:AC26",
            2: "AE1:BG26",
            3: "A28:AC53",
            4: "AE28:BG53",
        }

        for (
            position,
            area,
        ) in blocks.items():

            if position not in used:

                excel.clear_range(
                    sheet,
                    area,
                )

    # ---------------------------------------------------------

    def build(
        self,
        labels: list[LabelModel],
        output_file: str,
        positions: list[int],
    ):

        excel = ExcelCom()

        excel.open(
            str(self.template)
        )

        try:

            self.fill_page(
                excel,
                labels,
                positions,
            )

            excel.save_as(
                output_file,
            )

        finally:

            excel.close()

    # ---------------------------------------------------------

    def export_pdf(
        self,
        labels: list[LabelModel],
        pdf_file: str,
        positions: list[int],
    ):
        """
        Экспорт в PDF.

        Здесь пока сохраняем прежнее поведение:
        PDF формируется по выбранной области.

        Это не влияет на позиционирование
        при печати на реальном листе.
        """

        excel = ExcelCom()

        excel.open(
            str(self.template)
        )

        try:

            self.fill_page(
                excel,
                labels,
                positions,
            )

            sheet = (
                excel.specification_sheet()
            )

            excel.export_pdf(
                sheet,
                pdf_file,
                self.print_area(
                    positions
                ),
            )

        finally:

            excel.close()

    # ---------------------------------------------------------

    def print_document(
        self,
        labels: list[LabelModel],
        positions: list[int],
        printer_name: str | None = None,
    ):
        """
        Печать спецификаций.

        Всегда печатается полный макет листа
        из четырёх позиций.

        Например, если выбрана позиция 4:

            [ пусто ] [ пусто ]
            [ пусто ] [ спецификация ]

        Excel получает всю область A1:BG53,
        поэтому позиция 4 не растягивается
        на место позиции 1.
        """

        with temporary_default_printer(
            printer_name
        ):

            excel = ExcelCom()

            excel.open(
                str(self.template)
            )

            try:

                # -----------------------------------------
                # Записываем данные именно
                # в выбранные позиции.
                # -----------------------------------------

                self.fill_page(
                    excel,
                    labels,
                    positions,
                )

                # -----------------------------------------
                # Очищаем остальные позиции шаблона.
                # -----------------------------------------

                self.clear_unused_blocks(
                    excel,
                    positions,
                )

                sheet = (
                    excel.specification_sheet()
                )

                # -----------------------------------------
                # ВАЖНО:
                #
                # Не используем:
                #
                # self.print_area(positions)
                #
                # потому что тогда Excel воспринимает
                # выбранный блок как отдельную страницу
                # и переносит его в начало листа.
                #
                # Печатаем весь физический макет 2 x 2.
                # -----------------------------------------

                excel.print(
                    sheet,
                    self.full_print_area(),
                )

            finally:

                excel.close()
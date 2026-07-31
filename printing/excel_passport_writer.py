from models.label_model import LabelModel


class ExcelPassportWriter:
    """
    Заполняет один паспорт изделия.
    """

    def __init__(
        self,
        sheet,
        coordinates: dict[str, str],
    ):

        self.sheet = sheet
        self.coords = coordinates

    # ---------------------------------------------------------

    def write(
        self,
        label: LabelModel,
    ):

        self.write_title(label)
        self.write_date(label)
        self.write_serial(label)
        self.write_article(label)
        self.write_model(label)
        self.write_components(label)
        self.write_warranty(label)

    # ---------------------------------------------------------

    def write_title(
        self,
        label: LabelModel,
    ):

        self.write_cell(
            "TITLE",
            label.title,
        )

    # ---------------------------------------------------------

    def write_date(
        self,
        label: LabelModel,
    ):
        """
        Дата производства выводится
        в двух местах шаблона паспорта.

        В ячейки записывается только сама дата,
        без текста "ДАТА ПРОИЗВОДСТВА:".
        """

        date = (
            getattr(
                label,
                "date",
                "",
            )
            or ""
        )

        for cell in (
            "V7",
            "AD41",
        ):

            self.sheet.Range(
                cell
            ).Value = date

    # ---------------------------------------------------------

    def write_serial(
        self,
        label: LabelModel,
    ):

        for cell in (
            "O1",
            "D7",
            "AD35",
            "AP41",
        ):

            self.sheet.Range(
                cell
            ).Value = label.serial

    # ---------------------------------------------------------

    def write_model(
        self,
        label: LabelModel,
    ):

        self.write_cell(
            "MODEL",
            label.internal_name,
        )

    # ---------------------------------------------------------

    def write_cell(
        self,
        key: str,
        value,
    ):

        if value is None:
            return

        cell = self.coords.get(
            key
        )

        if not cell:
            return

        self.sheet.Range(
            cell
        ).Value = value

    # ---------------------------------------------------------

    def write_article(
        self,
        label: LabelModel,
    ):

        for cell in (
            "P7",
            "AJ41",
        ):

            self.sheet.Range(
                cell
            ).Value = label.article_code

    # ---------------------------------------------------------

    def write_components(
        self,
        label: LabelModel,
    ):
        """
        Печатает полный состав изделия.

        B  - полное наименование комплектующего
        AA - количество
        AD - серийный номер

        Серийный номер больше не добавляется
        к тексту наименования.
        """

        row = 19

        items = getattr(
            label,
            "items",
            [],
        )

        # =================================================
        # Новые изделия
        # =================================================

        if items:

            for item in items:

                if row > 27:
                    break

                name = (
                    getattr(
                        item,
                        "name",
                        "",
                    )
                    or ""
                ).strip()

                if not name:
                    continue

                serial_number = (
                    getattr(
                        item,
                        "serial_number",
                        "",
                    )
                    or ""
                ).strip()

                quantity = getattr(
                    item,
                    "quantity",
                    1,
                )

                try:

                    quantity = int(
                        quantity
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    quantity = 1

                if quantity < 1:

                    quantity = 1

                # -----------------------------------------
                # Полное наименование
                # -----------------------------------------

                self.sheet.Range(
                    f"B{row}"
                ).Value = name

                # -----------------------------------------
                # Количество
                # -----------------------------------------

                self.sheet.Range(
                    f"AA{row}"
                ).Value = quantity

                # -----------------------------------------
                # Серийный номер
                #
                # Отдельный столбец справа.
                # Если S/N не введён, оставляем пусто.
                # -----------------------------------------

                self.sheet.Range(
                    f"U{row}"
                ).Value = serial_number

                row += 1

            return

        # =================================================
        # Старые изделия
        #
        # Если в старой записи нет build_items,
        # используем сокращённые сохранённые поля.
        # =================================================

        component_fields = (
            "cpu",
            "cooler",
            "motherboard",
            "ram",
            "storage",
            "case",
            "psu",
            "gpu",
        )

        for field in component_fields:

            if row > 27:
                break

            value = getattr(
                label,
                field,
                "",
            )

            if not value:
                continue

            self.sheet.Range(
                f"B{row}"
            ).Value = value

            self.sheet.Range(
                f"AA{row}"
            ).Value = 1

            # Для старых изделий S/N отсутствует.

            self.sheet.Range(
                f"U{row}"
            ).Value = ""

            row += 1

        # -------------------------------------------------
        # ОС старого изделия
        # -------------------------------------------------

        operating_system = getattr(
            label,
            "operating_system",
            "",
        )

        if (
            operating_system
            and row <= 27
        ):

            self.sheet.Range(
                f"B{row}"
            ).Value = operating_system

            self.sheet.Range(
                f"AA{row}"
            ).Value = 1

            self.sheet.Range(
                f"AD{row}"
            ).Value = ""

    # ---------------------------------------------------------

    def write_warranty(
        self,
        label: LabelModel,
    ):

        months = getattr(
            label,
            "warranty_months",
            36,
        )

        try:

            months = int(
                months
            )

        except (
            TypeError,
            ValueError,
        ):

            months = 36

        warranty = (
            f"{months} месяцев"
        )

        self.sheet.Range(
            "G48"
        ).Value = warranty

        self.sheet.Range(
            "AS35"
        ).Value = warranty
class SpecificationWriter:
    """
    Заполняет один блок производственной спецификации.

    Для перечня комплектующих используются
    исходные позиции из label.items.

    Поэтому в спецификацию и паспорт попадает
    полное наименование комплектующего,
    полученное из исходной спецификации 1С.

    Сокращённые поля label.cpu, label.ram,
    label.storage и т.д. используются только
    для формирования названия модели и других
    компактных представлений.
    """

    # ---------------------------------------------------------

    def __init__(
        self,
        sheet=None,
        coordinates=None,
    ):

        self.sheet = sheet
        self.coords = coordinates or {}

    # ---------------------------------------------------------

    def write(
        self,
        label,
    ):

        self._write_header(
            label
        )

        self._write_components(
            label
        )

    # ---------------------------------------------------------

    def _write_header(
        self,
        label,
    ):

        c = self.coords

        self.sheet.Range(
            c["TITLE"]
        ).Value = label.title

        self.sheet.Range(
            c["SERIAL"]
        ).Value = label.serial

        self.sheet.Range(
            c["MODEL"]
        ).Value = label.internal_name

        self.sheet.Range(
            c["ARTICLE"]
        ).Value = label.article_code

        self.sheet.Range(
            c["DATE"]
        ).Value = (
            f"ДАТА ПРОИЗВОДСТВА: {label.date}"
        )

    # ---------------------------------------------------------

    def get_rows(
        self,
        label,
    ):
        """
        Возвращает строки состава изделия.

        Формат:

            [
                (полное_наименование, количество),
                ...
            ]

        Главным источником является label.items.

        Это полный исходный состав компьютера,
        включая:

        - полное название комплектующего;
        - количество;
        - OTHER;
        - операционную систему;
        - монитор и другие дополнительные позиции.

        Серийные номера здесь пока намеренно
        не выводятся.
        """

        rows = []

        # =================================================
        # Полный состав изделия
        # =================================================

        items = getattr(
            label,
            "items",
            [],
        )

        for item in items:

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

            rows.append(
                (
                    name,
                    quantity,
                )
            )

        # =================================================
        # Совместимость со старыми изделиями
        # =================================================
        #
        # Старые записи в базе могут не иметь build_items.
        #
        # В таком случае используем старые сокращённые
        # поля, чтобы старые изделия по-прежнему
        # можно было распечатать.
        # =================================================

        if not rows:

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

                value = getattr(
                    label,
                    field,
                    "",
                )

                if value:

                    rows.append(
                        (
                            value,
                            1,
                        )
                    )

            # ---------------------------------------------
            # Операционная система старого изделия
            # ---------------------------------------------

            operating_system = getattr(
                label,
                "operating_system",
                "",
            )

            if operating_system:

                rows.append(
                    (
                        operating_system,
                        1,
                    )
                )

            # ---------------------------------------------
            # Старые дополнительные позиции
            # ---------------------------------------------

            additional_items = getattr(
                label,
                "additional_items",
                [],
            )

            for item in additional_items:

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

                quantity = getattr(
                    item,
                    "quantity",
                    1,
                )

                rows.append(
                    (
                        name,
                        quantity,
                    )
                )

        return rows

    # ---------------------------------------------------------

    def _write_components(
        self,
        label,
    ):

        c = self.coords

        first_component = (
            c["FIRST_COMPONENT"]
        )

        first_qty = (
            c["FIRST_QTY"]
        )

        component_column = "".join(
            filter(
                str.isalpha,
                first_component,
            )
        )

        qty_column = "".join(
            filter(
                str.isalpha,
                first_qty,
            )
        )

        row = int(
            "".join(
                filter(
                    str.isdigit,
                    first_component,
                )
            )
        )

        for (
            name,
            quantity,
        ) in self.get_rows(label):

            self.sheet.Range(
                f"{component_column}{row}"
            ).Value = name

            self.sheet.Range(
                f"{qty_column}{row}"
            ).Value = quantity

            row += 1
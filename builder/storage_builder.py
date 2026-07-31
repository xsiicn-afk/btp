import re


class StorageBuilder:
    """
    Формирует краткое описание накопителя.

    Примеры:

        1000 ГБ M.2 NVMe накопитель Kingston NV3
        -> SSD NVMe 1TB

        Накопитель SSD Kingston NV3 4000GB M.2
        -> SSD NVMe 4TB

        SSD SATA 512GB
        -> SSD SATA 512GB

        HDD 2000GB
        -> HDD 2TB

    Значения TBW не считаются объёмом накопителя.
    """

    def build(
        self,
        full_name: str,
    ) -> str:

        storage_type = self._extract_type(
            full_name
        )

        capacity = self._extract_capacity(
            full_name
        )

        parts = []

        if storage_type:

            parts.append(
                storage_type
            )

        if capacity:

            parts.append(
                capacity
            )

        return " ".join(
            parts
        ).strip()

    # --------------------------------------------------

    @staticmethod
    def _extract_type(
        text: str,
    ) -> str:

        upper = text.upper()

        if "HDD" in upper:

            return "HDD"

        if (
            "NVME" in upper
            or "NVM EXPRESS" in upper
        ):

            return "SSD NVMe"

        if "M.2" in upper:

            return "SSD M.2"

        if (
            "SSD" in upper
            and "SATA" in upper
        ):

            return "SSD SATA"

        if "SSD" in upper:

            return "SSD"

        return "SSD"

    # --------------------------------------------------

    @staticmethod
    def _extract_capacity(
        text: str,
    ) -> str:
        """
        Ищет основной объём накопителя.

        В первую очередь рассматриваем часть строки
        ДО подробных характеристик в квадратных
        скобках.

        Это исключает:

            TBW - 320 ТБ

        из определения ёмкости накопителя.
        """

        # Основное название товара обычно находится
        # до первой квадратной скобки.

        main_part = text.split(
            "[",
            1,
        )[0]

        capacity = (
            StorageBuilder._find_capacity(
                main_part
            )
        )

        if capacity:

            return capacity

        # Если в основной части объём почему-то
        # отсутствует, используем всю строку,
        # предварительно удалив TBW.

        clean_text = re.sub(
            r"TBW\s*[-:–—]?\s*"
            r"\d+(?:[.,]\d+)?\s*"
            r"(?:TB|ТБ|GB|ГБ)",
            "",
            text,
            flags=re.IGNORECASE,
        )

        return StorageBuilder._find_capacity(
            clean_text
        )

    # --------------------------------------------------

    @staticmethod
    def _find_capacity(
        text: str,
    ) -> str:

        """
        Возвращает первое найденное значение
        ёмкости в порядке появления в строке.
        """

        pattern = re.compile(
            r"(\d+(?:[.,]\d+)?)\s*"
            r"(TB|ТБ|GB|ГБ)\b",
            re.IGNORECASE,
        )

        match = pattern.search(
            text
        )

        if not match:

            return ""

        value_text = (
            match.group(1)
            .replace(",", ".")
        )

        unit = (
            match.group(2)
            .upper()
        )

        # ---------------------------------------------
        # TB / ТБ
        # ---------------------------------------------

        if unit in (
            "TB",
            "ТБ",
        ):

            value = float(
                value_text
            )

            if value.is_integer():

                return (
                    f"{int(value)}TB"
                )

            return (
                f"{value:g}TB"
            )

        # ---------------------------------------------
        # GB / ГБ
        # ---------------------------------------------

        value = float(
            value_text
        )

        # 1000 GB -> 1TB
        # 2000 GB -> 2TB
        # 4000 GB -> 4TB

        if (
            value >= 1000
            and value % 1000 == 0
        ):

            return (
                f"{int(value / 1000)}TB"
            )

        if value.is_integer():

            return (
                f"{int(value)}GB"
            )

        return (
            f"{value:g}GB"
        )
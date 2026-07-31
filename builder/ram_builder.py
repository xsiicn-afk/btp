import re


class RamBuilder:
    """
    Формирует краткое описание
    оперативной памяти.

    Примеры:

        DDR5 32GB 5600MHz
        -> DDR5 32GB 5600MHz

        16 ГБ [DDR5, 8 ГБx2 шт, 5600 МГц]
        -> DDR5 16GB 5600MHz

        DDR4 16GB 3200MHz
        (в количестве 2 шт.)
        -> DDR4 32GB 3200MHz (2x16GB)
    """

    def build(
        self,
        full_name: str,
        quantity: int,
    ) -> str:

        memory_type = (
            self._extract_type(
                full_name
            )
        )

        capacity = (
            self._extract_capacity(
                full_name
            )
        )

        speed = (
            self._extract_speed(
                full_name
            )
        )

        total_capacity = capacity

        if (
            capacity > 0
            and quantity > 1
        ):

            total_capacity = (
                capacity * quantity
            )

        parts = []

        if memory_type:
            parts.append(
                memory_type
            )

        if total_capacity:
            parts.append(
                f"{total_capacity}GB"
            )

        if speed:
            parts.append(
                f"{speed}MHz"
            )

        if (
            quantity > 1
            and capacity > 0
        ):

            parts.append(
                f"({quantity}x{capacity}GB)"
            )

        return " ".join(
            parts
        )

    # --------------------------------------------------

    @staticmethod
    def _extract_type(
        text: str,
    ) -> str:

        match = re.search(
            r"\bDDR\s*([3-6])\b",
            text,
            re.IGNORECASE,
        )

        if not match:
            return ""

        return (
            f"DDR{match.group(1)}"
        )

    # --------------------------------------------------

    @staticmethod
    def _extract_capacity(
        text: str,
    ) -> int:
        """
        Берём общий объём товарной позиции.

        Например:

            ADATA ... 16 ГБ
            [DDR5, 8 ГБx2 шт, ...]

        Здесь объём позиции = 16 ГБ,
        а 8 ГБx2 описывает внутренний
        состав комплекта.
        """

        matches = re.findall(
            r"(\d+)\s*(?:GB|ГБ)\b",
            text,
            re.IGNORECASE,
        )

        if not matches:
            return 0

        return int(
            matches[0]
        )

    # --------------------------------------------------

    @staticmethod
    def _extract_speed(
        text: str,
    ) -> int:

        match = re.search(
            r"(\d{3,5})\s*"
            r"(?:MHZ|МГЦ)\b",
            text,
            re.IGNORECASE,
        )

        if not match:
            return 0

        return int(
            match.group(1)
        )
import re


class CpuBuilder:
    """
    Формирует краткое название процессора.

    Примеры:

        Процессор AMD Ryzen 5 7500F OEM [...]
        -> AMD Ryzen 5 7500F

        Процессор Intel Core i5-12400F BOX [...]
        -> Intel Core i5-12400F

        Процессор Intel Core 5 12400F
        -> Intel Core i5 12400F
    """

    def build(
        self,
        full_name: str,
    ) -> str:

        text = full_name.strip()

        # -------------------------------------------------
        # Убираем название категории
        # -------------------------------------------------

        text = re.sub(
            r"^Процессор\s+",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # -------------------------------------------------
        # Всё в квадратных скобках —
        # подробные характеристики процессора.
        # Для короткого имени они не нужны.
        # -------------------------------------------------

        text = re.sub(
            r"\s*\[.*$",
            "",
            text,
        )

        # -------------------------------------------------
        # OEM / BOX / TRAY не являются частью
        # модели процессора.
        # -------------------------------------------------

        text = re.sub(
            r"\b(OEM|BOX|TRAY)\b",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # -------------------------------------------------
        # Нормализуем некоторые варианты Intel Core
        # -------------------------------------------------

        text = re.sub(
            r"\bIntel\s+Core\s+3\b",
            "Intel Core i3",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\bIntel\s+Core\s+5\b",
            "Intel Core i5",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\bIntel\s+Core\s+7\b",
            "Intel Core i7",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\bIntel\s+Core\s+9\b",
            "Intel Core i9",
            text,
            flags=re.IGNORECASE,
        )

        # -------------------------------------------------
        # Убираем лишние пробелы
        # -------------------------------------------------

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()
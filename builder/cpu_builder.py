import re


class CpuBuilder:
    """Формирует краткое название процессора."""

    def build(self, full_name: str) -> str:
        text = full_name

        # Убираем служебные слова
        text = text.replace("Процессор", "").strip()

        # Intel Core 5 -> Core i5
        text = text.replace("Intel Core 3", "Core i3")
        text = text.replace("Intel Core 5", "Core i5")
        text = text.replace("Intel Core 7", "Core i7")
        text = text.replace("Intel Core 9", "Core i9")

        # Ryzen оставляем как есть
        text = text.replace("AMD ", "")

        # Убираем лишние пробелы
        text = re.sub(r"\s+", " ", text)

        return text.strip()
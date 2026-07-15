import re


class BaseBuilder:
    """
    Базовый класс для всех Builder'ов.
    Содержит общие методы обработки текста.
    """

    @staticmethod
    def normalize_spaces(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def remove_prefix(text: str, prefix: str) -> str:
        if text.lower().startswith(prefix.lower()):
            return text[len(prefix):].strip()
        return text

    @staticmethod
    def first_words(text: str, count: int) -> str:
        words = text.split()
        return " ".join(words[:count])

    @staticmethod
    def extract_power(text: str) -> str:
        match = re.search(r"(\d{3,4})\s*W", text, re.IGNORECASE)
        return f"{match.group(1)}W" if match else ""

    @staticmethod
    def extract_memory(text: str) -> str:
        match = re.search(r"(\d+)\s*Gb", text, re.IGNORECASE)
        return f"{match.group(1)}GB" if match else ""

    @staticmethod
    def remove_after_slash(text: str) -> str:
        return text.split("/")[0].strip()
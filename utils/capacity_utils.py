import re


def format_capacity(size_gb: int) -> str:
    """
    Преобразует объем в красивый формат.
    """

    if size_gb >= 1000 and size_gb % 1000 == 0:
        return f"{size_gb // 1000}TB"

    return f"{size_gb}GB"


def extract_capacity(text: str) -> int | None:
    """
    Извлекает объем накопителя из строки.
    """

    match = re.search(r"(\d+)\s*G[Bb]", text)

    if match:
        return int(match.group(1))

    return None
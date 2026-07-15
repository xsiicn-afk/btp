from dataclasses import dataclass


@dataclass
class AdditionalItem:
    """
    Дополнительная комплектация,
    не входящая в базовую конфигурацию.
    """

    name: str = ""

    quantity: int = 1
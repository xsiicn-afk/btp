from dataclasses import dataclass

from models.category import Category


@dataclass
class Item:
    """
    Одна позиция конфигурации компьютера.

    db_id используется для уже сохранённых
    комплектующих из таблицы build_items.

    Для новой конфигурации db_id остаётся None.
    """

    category: Category

    name: str

    quantity: int = 1

    serial_number: str = ""

    db_id: int | None = None
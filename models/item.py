from dataclasses import dataclass

from models.category import Category


@dataclass
class Item:
    category: Category
    name: str
    quantity: int = 1
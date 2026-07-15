from dataclasses import dataclass, field

from models.item import Item


@dataclass
class Configuration:
    items: list[Item] = field(default_factory=list)

    article: str = ""

    serial: str = ""

    date: str = ""

    model_name: str = "Системный блок ByTop PE"
    
    # -------------------------------------------------
    # Программное обеспечение
    # -------------------------------------------------
    operating_system: str = ""
    
    def add_item(self, item: Item):
        self.items.append(item)

    def get_items(self, category):
        return [i for i in self.items if i.category == category]
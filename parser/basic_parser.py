import re

from models.configuration import Configuration
from models.item import Item
from models.category import Category


class BasicParser:

    def parse(self, text: str) -> Configuration:

        configuration = Configuration()

        lines = text.splitlines()

        for line in lines:

            clean = line.strip()

            if not clean:
                continue

            upper = clean.upper()

            quantity = self.extract_quantity(clean)

            if upper.startswith("ПРОЦЕССОР"):
                configuration.add_item(Item(Category.CPU, clean, quantity))
                continue

            if upper.startswith("МАТЕРИНСК"):
                configuration.add_item(Item(Category.MOTHERBOARD, clean, quantity))
                continue

            if upper.startswith("КУЛЕР") or upper.startswith("КУЛЕРЫ"):
                configuration.add_item(Item(Category.COOLER, clean, quantity))
                continue

            if upper.startswith("МОДУЛЬ ОПЕРАТИВНОЙ ПАМЯТИ"):
                configuration.add_item(Item(Category.RAM, clean, quantity))
                continue

            if upper.startswith("НАКОПИТЕЛЬ"):
                configuration.add_item(Item(Category.STORAGE, clean, quantity))
                continue

            if upper.startswith("ВИДЕОАДАПТЕР"):
                configuration.add_item(Item(Category.GPU, clean, quantity))
                continue

            if upper.startswith("БЛОК ПИТАНИЯ"):
                configuration.add_item(Item(Category.PSU, clean, quantity))
                continue

            if upper.startswith("КОРПУС"):
                configuration.add_item(Item(Category.CASE, clean, quantity))
                continue

            configuration.add_item(Item(Category.OTHER, clean, quantity))

        return configuration

    @staticmethod
    def extract_quantity(text: str) -> int:
        """
        Ищет '(в количестве N шт.)'
        """

        match = re.search(r"(\d+)\s*шт", text, re.IGNORECASE)

        if match:
            return int(match.group(1))

        return 1
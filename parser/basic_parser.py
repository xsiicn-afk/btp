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

            #
            # Служебная информация
            #

            self.parse_metadata(
                configuration,
                clean,
            )

            self.parse_operating_system(
                configuration,
                clean,
            )

            upper = clean.upper()

            quantity = self.extract_quantity(clean)

            #
            # Процессор
            #

            if upper.startswith("ПРОЦЕССОР"):
                configuration.add_item(
                    Item(Category.CPU, clean, quantity)
                )
                continue

            #
            # Материнская плата
            #

            if upper.startswith("МАТЕРИНСК"):
                configuration.add_item(
                    Item(Category.MOTHERBOARD, clean, quantity)
                )
                continue

            #
            # Кулер
            #

            if (
                upper.startswith("КУЛЕР")
                or upper.startswith("КУЛЕРЫ")
            ):
                configuration.add_item(
                    Item(Category.COOLER, clean, quantity)
                )
                continue

            #
            # RAM
            #

            if (
                upper.startswith("МОДУЛЬ ОПЕРАТИВНОЙ ПАМЯТИ")
                or upper.startswith("ПАМЯТЬ")
                or upper.startswith("DIMM")
            ):
                configuration.add_item(
                    Item(Category.RAM, clean, quantity)
                )
                continue

            #
            # SSD/HDD
            #

            if upper.startswith("НАКОПИТЕЛЬ"):
                configuration.add_item(
                    Item(Category.STORAGE, clean, quantity)
                )
                continue

            #
            # Видео
            #

            if (
                upper.startswith("ВИДЕОАДАПТЕР")
                or upper.startswith("ВИДЕОКАРТА")
            ):
                configuration.add_item(
                    Item(Category.GPU, clean, quantity)
                )
                continue

            #
            # Блок питания
            #

            if upper.startswith("БЛОК ПИТАНИЯ"):
                configuration.add_item(
                    Item(Category.PSU, clean, quantity)
                )
                continue

            #
            # Корпус
            #

            if upper.startswith("КОРПУС"):
                configuration.add_item(
                    Item(Category.CASE, clean, quantity)
                )
                continue

            #
            # Остальное
            #

            configuration.add_item(
                Item(Category.OTHER, clean, quantity)
            )

        return configuration

    # --------------------------------------------------

    @staticmethod
    def parse_metadata(
        configuration: Configuration,
        line: str,
    ):

        upper = line.upper()

        #
        # Серийный номер
        #

        if "S/N" in upper:

            match = re.search(
                r"(\d{5,})",
                line,
            )

            if match:
                configuration.serial = match.group(1)

        #
        # Артикул
        #

        if "АРТ" in upper:

            match = re.search(
                r"(\d{3}\s?\d{3}|\d{6})",
                line,
            )

            if match:
                configuration.article = (
                    match.group(1).replace(" ", "")
                )

        #
        # Дата
        #

        if "ДАТА ПРОИЗВОДСТВА" in upper:

            if ":" in line:
                configuration.date = (
                    line.split(":", 1)[1].strip()
                )
            else:
                configuration.date = line.strip()

    # --------------------------------------------------

    @staticmethod
    def parse_operating_system(
        configuration: Configuration,
        line: str,
    ):

        upper = line.upper()

        #
        # Windows
        #

        if "WINDOWS 11 PRO" in upper:
            configuration.operating_system = "Windows 11 Pro"
            return

        if "WINDOWS 11 HOME" in upper:
            configuration.operating_system = "Windows 11 Home"
            return

        if "WINDOWS 10 PRO" in upper:
            configuration.operating_system = "Windows 10 Pro"
            return

        if "WINDOWS 10 HOME" in upper:
            configuration.operating_system = "Windows 10 Home"
            return

        #
        # Astra Linux
        #

        if "ASTRA" in upper:
            configuration.operating_system = "Astra Linux"
            return

        #
        # BaseALT
        #

        if (
            "BASEALT" in upper
            or "BASE ALT" in upper
        ):
            configuration.operating_system = "BaseALT"
            return

        #
        # РЕД ОС
        #

        if (
            "РЕД ОС" in upper
            or "RED OS" in upper
        ):
            configuration.operating_system = "РЕД ОС"

    # --------------------------------------------------

    @staticmethod
    def extract_quantity(text: str) -> int:
        """
        Ищет количество компонентов.
        """

        match = re.search(
            r"(\d+)\s*шт",
            text,
            re.IGNORECASE,
        )

        if match:
            return int(match.group(1))

        return 1
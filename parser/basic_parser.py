import re

from models.configuration import Configuration
from models.item import Item
from models.category import Category


class BasicParser:

    def parse(
        self,
        text: str,
    ) -> Configuration:

        configuration = Configuration()

        lines = text.splitlines()

        for line in lines:

            clean = line.strip()

            if not clean:
                continue

            # ---------------------------------------------
            # Метаданные
            # ---------------------------------------------

            self.parse_metadata(
                configuration,
                clean,
            )

            # ---------------------------------------------
            # Операционная система
            #
            # ОС теперь:
            #
            # 1. сохраняется коротким названием в
            #    configuration.operating_system;
            #
            # 2. добавляется полноценной позицией Item
            #    с исходным полным названием;
            #
            # 3. получает отдельную категорию OS;
            #
            # 4. поэтому появляется в правой таблице
            #    и для неё можно вводить S/N / ключ.
            # ---------------------------------------------

            if self.parse_operating_system(
                configuration,
                clean,
            ):

                quantity = self.extract_quantity(
                    clean
                )

                configuration.add_item(
                    Item(
                        Category.OS,
                        clean,
                        quantity,
                    )
                )

                continue

            upper = clean.upper()

            quantity = self.extract_quantity(
                clean
            )

            # ---------------------------------------------
            # Процессор
            # ---------------------------------------------

            if upper.startswith(
                "ПРОЦЕССОР"
            ):

                configuration.add_item(
                    Item(
                        Category.CPU,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Материнская плата
            # ---------------------------------------------

            if upper.startswith(
                "МАТЕРИНСК"
            ):

                configuration.add_item(
                    Item(
                        Category.MOTHERBOARD,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Кулер
            # ---------------------------------------------

            if (
                upper.startswith("КУЛЕР")
                or upper.startswith("КУЛЕРЫ")
            ):

                configuration.add_item(
                    Item(
                        Category.COOLER,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Накопитель
            # ---------------------------------------------

            if self.is_storage(
                upper
            ):

                configuration.add_item(
                    Item(
                        Category.STORAGE,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Оперативная память
            # ---------------------------------------------

            if self.is_ram(
                upper
            ):

                configuration.add_item(
                    Item(
                        Category.RAM,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Видеокарта
            # ---------------------------------------------

            if (
                upper.startswith(
                    "ВИДЕОАДАПТЕР"
                )
                or upper.startswith(
                    "ВИДЕОКАРТА"
                )
            ):

                configuration.add_item(
                    Item(
                        Category.GPU,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Блок питания
            # ---------------------------------------------

            if upper.startswith(
                "БЛОК ПИТАНИЯ"
            ):

                configuration.add_item(
                    Item(
                        Category.PSU,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Корпус
            # ---------------------------------------------

            if upper.startswith(
                "КОРПУС"
            ):

                configuration.add_item(
                    Item(
                        Category.CASE,
                        clean,
                        quantity,
                    )
                )

                continue

            # ---------------------------------------------
            # Всё остальное
            # ---------------------------------------------

            configuration.add_item(
                Item(
                    Category.OTHER,
                    clean,
                    quantity,
                )
            )

        return configuration

    # --------------------------------------------------

    @staticmethod
    def is_storage(
        upper: str,
    ) -> bool:

        storage_words = (
            "НАКОПИТЕЛЬ",
            "SSD",
            "NVME",
            "NVM EXPRESS",
            "HDD",
        )

        return any(
            word in upper
            for word in storage_words
        )

    # --------------------------------------------------

    @staticmethod
    def is_ram(
        upper: str,
    ) -> bool:

        ram_markers = (
            "ОПЕРАТИВНАЯ ПАМЯТЬ",
            "МОДУЛЬ ОПЕРАТИВНОЙ ПАМЯТИ",
            "МОДУЛЬ ПАМЯТИ",
        )

        if any(
            marker in upper
            for marker in ram_markers
        ):
            return True

        if upper.startswith(
            "DIMM"
        ):
            return True

        if upper.startswith(
            "ПАМЯТЬ DDR"
        ):
            return True

        return False

    # --------------------------------------------------

    @staticmethod
    def parse_metadata(
        configuration: Configuration,
        line: str,
    ):

        upper = line.upper()

        if "S/N" in upper:

            match = re.search(
                r"(\d{5,})",
                line,
            )

            if match:

                configuration.serial = (
                    match.group(1)
                )

        if "АРТ" in upper:

            match = re.search(
                r"(\d{3}\s?\d{3}|\d{6})",
                line,
            )

            if match:

                configuration.article = (
                    match.group(1)
                    .replace(
                        " ",
                        "",
                    )
                )

        if (
            "ДАТА ПРОИЗВОДСТВА"
            in upper
        ):

            if ":" in line:

                configuration.date = (
                    line.split(
                        ":",
                        1,
                    )[1].strip()
                )

            else:

                configuration.date = (
                    line.strip()
                )

    # --------------------------------------------------

    @staticmethod
    def parse_operating_system(
        configuration: Configuration,
        line: str,
    ) -> bool:

        """
        Определяет ОС и записывает её короткое
        название для формирования имени ПК.

        Полная исходная строка добавляется
        в configuration.items методом parse().
        """

        upper = line.upper()

        # Windows 11

        if (
            "WINDOWS 11 PROFESSIONAL" in upper
            or "WINDOWS 11 PRO" in upper
            or "WIN 11 PRO" in upper
        ):

            configuration.operating_system = (
                "Windows 11 Pro"
            )

            return True

        if (
            "WINDOWS 11 HOME" in upper
            or "WIN 11 HOME" in upper
        ):

            configuration.operating_system = (
                "Windows 11 Home"
            )

            return True

        if (
            "WINDOWS 11" in upper
            or "WIN 11" in upper
        ):

            configuration.operating_system = (
                "Windows 11"
            )

            return True

        # Windows 10

        if (
            "WINDOWS 10 PROFESSIONAL" in upper
            or "WINDOWS 10 PRO" in upper
            or "WIN 10 PRO" in upper
        ):

            configuration.operating_system = (
                "Windows 10 Pro"
            )

            return True

        if (
            "WINDOWS 10 HOME" in upper
            or "WIN 10 HOME" in upper
        ):

            configuration.operating_system = (
                "Windows 10 Home"
            )

            return True

        if (
            "WINDOWS 10" in upper
            or "WIN 10" in upper
        ):

            configuration.operating_system = (
                "Windows 10"
            )

            return True

        # Astra Linux

        if (
            "ASTRA LINUX" in upper
            or "АСТРА ЛИНУКС" in upper
            or upper.startswith("ASTRA ")
        ):

            configuration.operating_system = (
                "Astra Linux"
            )

            return True

        # Альт / BaseALT

        if (
            "АЛЬТ ЛИНУКС" in upper
            or "ALT LINUX" in upper
            or "ALT WORKSTATION" in upper
            or "АЛЬТ РАБОЧАЯ СТАНЦИЯ" in upper
            or "BASEALT" in upper
            or "BASE ALT" in upper
            or "БАЗАЛЬТ СПО" in upper
        ):

            configuration.operating_system = (
                "Альт Linux"
            )

            return True

        # РЕД ОС

        if (
            "РЕД ОС" in upper
            or "RED OS" in upper
            or "REDOS" in upper
        ):

            configuration.operating_system = (
                "РЕД ОС"
            )

            return True

        # ROSA

        if (
            "ROSA LINUX" in upper
            or "РОСА ЛИНУКС" in upper
            or "ROSA CHROME" in upper
            or "РОСА ХРОМ" in upper
        ):

            configuration.operating_system = (
                "ROSA Linux"
            )

            return True

        # Calculate

        if "CALCULATE LINUX" in upper:

            configuration.operating_system = (
                "Calculate Linux"
            )

            return True

        # Ubuntu

        if "UBUNTU" in upper:

            configuration.operating_system = (
                "Ubuntu"
            )

            return True

        # Debian

        if "DEBIAN" in upper:

            configuration.operating_system = (
                "Debian"
            )

            return True

        # Fedora

        if "FEDORA" in upper:

            configuration.operating_system = (
                "Fedora"
            )

            return True

        return False

    # --------------------------------------------------

    @staticmethod
    def extract_quantity(
        text: str,
    ) -> int:

        patterns = (
            r"В\s+КОЛИЧЕСТВЕ\s+(\d+)\s*ШТ",
            r"КОЛИЧЕСТВО\s*[:\-]?\s*(\d+)\s*ШТ",
            r"КОЛ-ВО\s*[:\-]?\s*(\d+)\s*ШТ",
        )

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                return int(
                    match.group(1)
                )

        return 1
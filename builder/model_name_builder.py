class ModelNameBuilder:
    """
    Формирует короткое наименование компьютера.

    Пример:

    AMD Ryzen 5 7500F/
    DDR5 16GB/
    SSD NVMe 1TB/
    GeForce RTX 5060 8GB GDDR7/
    mATX/
    750W/
    Windows 11 Pro
    """

    def build(
        self,
        cpu: str,
        ram: str,
        storage: str,
        gpu: str,
        case: str,
        psu: str,
        operating_system: str = "",
    ) -> str:

        parts = []

        # -------------------------------------------------
        # Процессор
        # -------------------------------------------------

        if cpu:

            parts.append(
                cpu.strip()
            )

        # -------------------------------------------------
        # Оперативная память
        #
        # Частоту RAM в короткое имя
        # компьютера не добавляем.
        # -------------------------------------------------

        ram_short = self._short_ram(
            ram
        )

        if ram_short:

            parts.append(
                ram_short
            )

        # -------------------------------------------------
        # Накопитель
        # -------------------------------------------------

        if storage:

            parts.append(
                storage.strip()
            )

        # -------------------------------------------------
        # Видеокарта
        # -------------------------------------------------

        if gpu:

            parts.append(
                gpu.strip()
            )

        # -------------------------------------------------
        # Корпус
        # -------------------------------------------------

        if case:

            parts.append(
                case.strip()
            )

        # -------------------------------------------------
        # Блок питания
        # -------------------------------------------------

        if psu:

            parts.append(
                psu.strip()
            )

        # -------------------------------------------------
        # Операционная система
        # -------------------------------------------------

        if operating_system:

            parts.append(
                operating_system.strip()
            )

        return "/".join(
            parts
        )

    # --------------------------------------------------

    @staticmethod
    def _short_ram(
        ram: str,
    ) -> str:

        if not ram:

            return ""

        parts = ram.split()

        result = []

        for part in parts:

            upper = part.upper()

            # ---------------------------------------------
            # Частота RAM
            #
            # 5600MHz убираем.
            # ---------------------------------------------

            if upper.endswith(
                "MHZ"
            ):
                continue

            # ---------------------------------------------
            # Количество модулей
            #
            # (2x16GB) также убираем
            # из короткого имени.
            # ---------------------------------------------

            if (
                part.startswith("(")
                and part.endswith(")")
            ):
                continue

            result.append(
                part
            )

        return " ".join(
            result
        ).strip()
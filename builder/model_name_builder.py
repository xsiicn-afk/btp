import re


class ModelNameBuilder:
    """
    Формирует производственное имя системного блока.

    Пример:

    Системный блок ByTop PE
    Ci5-12400/H610/
    DDR4 16GB 3200x2/
    SSD 512GB M.2/
    mATX/500W/W11Pro
    """

    PREFIX = "Системный блок ByTop PE "

    # --------------------------------------------------

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

        cpu_short = self._short_cpu(cpu)
        if cpu_short:
            parts.append(cpu_short)

        chipset = self._short_chipset(cpu)
        if chipset:
            parts.append(chipset)

        ram_short = self._short_ram(ram)
        if ram_short:
            parts.append(ram_short)

        storage_short = self._short_storage(storage)
        if storage_short:
            parts.append(storage_short)

        case_short = self._short_case(case)
        if case_short:
            parts.append(case_short)

        psu_short = self._short_psu(psu)
        if psu_short:
            parts.append(psu_short)

        os_short = self._short_os(operating_system)
        if os_short:
            parts.append(os_short)

        return self.PREFIX + "/".join(parts)

    # --------------------------------------------------

    @staticmethod
    def _short_cpu(value: str) -> str:

        if not value:
            return ""

        value = value.upper()

        intel = re.search(
            r"CORE\\s+I([3579])[- ]?(\\d{4,5}[A-Z]?)",
            value,
        )

        if intel:
            return f"Ci{intel.group(1)}-{intel.group(2)}"

        amd = re.search(
            r"RYZEN\\s+([3579])\\s+(\\d{4,5}[A-Z]?)",
            value,
        )

        if amd:
            return f"R{amd.group(1)}-{amd.group(2)}"

        return value.strip()

    # --------------------------------------------------

    @staticmethod
    def _short_chipset(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        match = re.search(
            r"\\b(H\\d{3}|B\\d{3}|Z\\d{3}|A\\d{3}|X\\d{3})",
            upper,
        )

        return match.group(1) if match else ""

    # --------------------------------------------------

    @staticmethod
    def _short_ram(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        mem_type = "DDR5" if "DDR5" in upper else "DDR4"

        size = re.search(r"(\\d+)\\s*GB", upper)
        freq = re.search(r"(\\d{4,5})\\s*MHZ", upper)
        count = re.search(r"X(\\d+)|\\((\\d+)X", upper)

        parts = [mem_type]

        if size:
            parts.append(f"{size.group(1)}GB")

        if freq:
            parts.append(freq.group(1))

        result = " ".join(parts)

        if count:
            modules = count.group(1) or count.group(2)
            result += f"x{modules}"

        return result

    # --------------------------------------------------

    @staticmethod
    def _short_storage(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        size = re.search(r"(\\d+)\\s*(TB|GB)", upper)

        if "M.2" in upper or "NVME" in upper:
            storage_type = "SSD"
            suffix = " M.2"
        else:
            storage_type = "SSD"
            suffix = ""

        if size:
            return f"{storage_type} {size.group(1)}{size.group(2)}{suffix}"

        return "SSD"

    # --------------------------------------------------

    @staticmethod
    def _short_case(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        if "MICROATX" in upper or "MATX" in upper:
            return "mATX"

        if "MINI-ITX" in upper or "ITX" in upper:
            return "ITX"

        if "ATX" in upper:
            return "ATX"

        return value.strip()

    # --------------------------------------------------

    @staticmethod
    def _short_psu(value: str) -> str:

        if not value:
            return ""

        match = re.search(r"(\\d{3,4})\\s*W", value.upper())

        return f"{match.group(1)}W" if match else value.strip()

    # --------------------------------------------------

    @staticmethod
    def _short_os(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        if "WINDOWS 11" in upper and "PRO" in upper:
            return "W11Pro"

        if "WINDOWS 10" in upper and "PRO" in upper:
            return "W10Pro"

        if "WINDOWS 11" in upper:
            return "W11"

        if "WINDOWS 10" in upper:
            return "W10"

        if "ASTRA" in upper:
            return "Astra"

        if "BASEALT" in upper or "BASE ALT" in upper:
            return "BaseALT"

        return value.strip()
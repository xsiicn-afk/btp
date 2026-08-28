import re

from services.template_service import TemplateService

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

        gpu_short = self._short_gpu(gpu)
        if gpu_short:
            parts.append(gpu_short)
        
        case_short = self._short_case(case)
        if case_short:
            parts.append(case_short)

        psu_short = self._short_psu(psu)
        if psu_short:
            parts.append(psu_short)

        os_short = self._short_os(operating_system)
        if os_short:
            parts.append(os_short)

        prefix = TemplateService().model_prefix().strip()

        result = "/".join(parts)

        if not result:
            return prefix

        return f"{prefix} {result}"

    # --------------------------------------------------

    @staticmethod
    def _short_cpu(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        # ---------------------------------------------
        # Intel Core Ultra 9 285 / 285K / 285KF
        # ---------------------------------------------

        ultra = re.search(
            r"CORE\s+ULTRA\s+([3579])\s+(\d{3}[A-Z]*)",
            upper,
        )

        if ultra:
            return f"CU{ultra.group(1)} {ultra.group(2)}"

        # ---------------------------------------------
        # Intel Core i5 12400F
        # ---------------------------------------------

        intel_i = re.search(
            r"CORE\s+I([3579])[- ]?(\d{4,5}[A-Z]?)",
            upper,
        )

        if intel_i:
            return f"Ci{intel_i.group(1)}-{intel_i.group(2)}"

        # ---------------------------------------------
        # Intel Core 5 12400F
        # Intel Core 7 14700K
        # ---------------------------------------------

        intel_new = re.search(
            r"CORE\s+([3579])\s+(\d{4,5}[A-Z]?)",
            upper,
        )

        if intel_new:
            return f"Ci{intel_new.group(1)}-{intel_new.group(2)}"

        # ---------------------------------------------
        # Intel Pentium G4400 / G6405 / G7400
        # ---------------------------------------------

        pentium = re.search(
            r"PENTIUM\s+([A-Z]\d{4,5}[A-Z]?)",
            upper,
        )

        if pentium:
            return f"Intel {pentium.group(1)}"

        # ---------------------------------------------
        # Intel Celeron G5905
        # ---------------------------------------------

        celeron = re.search(
            r"CELERON\s+([A-Z]?\d{4,5}[A-Z]?)",
            upper,
        )

        if celeron:
            return f"Intel {celeron.group(1)}"

        # ---------------------------------------------
        # AMD Ryzen 5 5600 / 7500F
        # ---------------------------------------------

        amd = re.search(
            r"RYZEN\s+([3579])\s+(\d{4,5}[A-Z]?)",
            upper,
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

        # Тип памяти
        mem_type = "DDR5" if "DDR5" in upper else "DDR4"

        # Берём первый указанный общий объём
        size_match = re.search(
            r"(\d+)\s*(?:GB|ГБ)",
            upper,
        )

        if not size_match:
            return mem_type

        total = int(size_match.group(1))

        # Частота
        freq_match = re.search(
            r"(\d{4,5})\s*(?:MHZ|МГЦ)",
            upper,
        )

        result = f"{mem_type} {total}GB"

        if freq_match:
            result += f" {freq_match.group(1)}"

        return result

    # --------------------------------------------------

    @staticmethod
    def _short_storage(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        # Все найденные объёмы
        matches = re.findall(r"(\d+)\s*(TB|GB)", upper)

        if not matches:
            return "SSD"

        # Берём первый найденный объём
        size, unit = matches[0]

        # Если объём в гигабайтах и кратен 1024 — переводим в TB
        if unit == "GB":
            gb = int(size)

            if gb % 1024 == 0 and gb >= 1024:
                size = str(gb // 1024)
                unit = "TB"

        suffix = " M.2" if ("M.2" in upper or "NVME" in upper) else ""

        return f"SSD {size}{unit}{suffix}"

# --------------------------------------------------

    @staticmethod
    def _short_gpu(value: str) -> str:

        if not value:
            return ""

        upper = value.upper()

        # RTX 5070 / RTX 5070 Ti / RTX 4060 Super
        rtx = re.search(
            r"RTX\s*(\d{4})(?:\s*(TI|SUPER))?",
            upper,
        )

        if rtx:

            model = rtx.group(1)
            suffix = rtx.group(2) or ""

            name = f"RTX{model}{suffix}"

            vram = re.search(r"(\d+)\s*GB", upper)

            if vram:
                return f"{name} {vram.group(1)}Gb"

            return name

        # GTX 1660 / 1650 Super
        gtx = re.search(
            r"GTX\s*(\d{3,4})(?:\s*(TI|SUPER))?",
            upper,
        )

        if gtx:

            model = gtx.group(1)
            suffix = gtx.group(2) or ""

            name = f"GTX{model}{suffix}"

            vram = re.search(r"(\d+)\s*GB", upper)

            if vram:
                return f"{name} {vram.group(1)}Gb"

            return name

        # Radeon RX 7800 XT / RX 7600
        rx = re.search(
            r"RX\s*(\d{4})(?:\s*(XT|XTX))?",
            upper,
        )

        if rx:

            model = rx.group(1)
            suffix = rx.group(2) or ""

            name = f"RX{model}{suffix}"

            vram = re.search(r"(\d+)\s*GB", upper)

            if vram:
                return f"{name} {vram.group(1)}Gb"

            return name

        return ""
    
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
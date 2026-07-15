import re


class HardwareInfo:
    """
    Универсальные методы извлечения характеристик оборудования.
    """

    @staticmethod
    def memory_gb(text: str) -> str:
        match = re.search(r"(\d+)\s*G[Bb]", text)
        if match:
            return match.group(1)
        return ""

    @staticmethod
    def power_w(text: str) -> str:
        match = re.search(r"(\d{3,4})\s*W", text, re.IGNORECASE)
        if match:
            return match.group(1)
        return ""

    @staticmethod
    def ddr(text: str) -> str:
        match = re.search(r"DDR([3456])", text, re.IGNORECASE)
        if match:
            return f"DDR{match.group(1)}"
        return ""

    @staticmethod
    def frequency(text: str) -> str:
        match = re.search(r"(\d{4,5})\s*MHz", text, re.IGNORECASE)
        if match:
            return match.group(1)
        return ""

    @staticmethod
    def socket(text: str) -> str:
        match = re.search(r"(1700|1851|1200|1151|AM4|AM5)", text, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return ""

    @staticmethod
    def form_factor(text: str) -> str:

        upper = text.upper()

        if "MICRO-ATX" in upper or "MATX" in upper:
            return "mATX"

        if "MINI-ITX" in upper:
            return "Mini-ITX"

        if "E-ATX" in upper:
            return "E-ATX"

        if "ATX" in upper:
            return "ATX"

        return ""

    @staticmethod
    def nvme(text: str) -> bool:
        upper = text.upper()
        return (
            "NVME" in upper
            or "PCI-E" in upper
            or "PCIE" in upper
            or "M.2" in upper
        )
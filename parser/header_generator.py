import re


class HeaderGenerator:
    def generate(self, parsed_data: dict) -> str:
        parts = []

        cpu = self._first(parsed_data.get("cpu"))
        ram = self._first(parsed_data.get("ram"))
        gpu = self._first(parsed_data.get("gpu"))

        if cpu:
            parts.append(self._clean_cpu(cpu))

        if ram:
            parts.append(self._clean_ram(ram))

        if gpu:
            parts.append(self._clean_gpu(gpu))

        # SSD / NVMe
        storage = self._find_storage(parsed_data.get("other", []))
        if storage:
            parts.append(storage)

        # PSU
        psu = self._find_psu(parsed_data.get("other", []))
        if psu:
            parts.append(psu)

        return " / ".join(parts)

    def _first(self, arr):
        return arr[0] if arr else None

    def _clean_cpu(self, text: str) -> str:
        return text

    def _clean_ram(self, text: str) -> str:
        return text

    def _clean_gpu(self, text: str) -> str:
        return text

    def _find_storage(self, items):
        for i in items:
            if "SSD" in i or "NVMe" in i or "M.2" in i:
                return i
        return None

    def _find_psu(self, items):
        for i in items:
            if "W" in i and any(x in i for x in ["PSU", "БП", "Power"]):
                return i
        return None
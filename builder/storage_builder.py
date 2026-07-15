import re


class StorageBuilder:
    """Формирует краткое описание накопителя."""

    def build(self, full_name: str) -> str:

        text = full_name.upper()

        # Тип накопителя
        storage_type = "SSD"

        if "NVME" in text:
            storage_type = "SSD NVMe"
        elif "M.2" in text:
            storage_type = "SSD M.2"
        elif "SSD" in text:
            storage_type = "SSD"
        elif "HDD" in text:
            storage_type = "HDD"

        # Объём
        capacity = ""

        match = re.search(r"(\d+)\s*G[Bb]", full_name)

        if match:
            size = int(match.group(1))

            if size >= 1000 and size % 1000 == 0:
                capacity = f"{size // 1000}TB"
            else:
                capacity = f"{size}GB"

        return f"{storage_type} {capacity}".strip()
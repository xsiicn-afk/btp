import re


class GpuBuilder:
    """
    Формирует короткое название видеокарты.
    """

    def build(self, text: str) -> str:

        text = text.replace("NVIDIA GeForce", "").strip()

        # RTX 5070
        match = re.search(r"(RTX)\s?(\d{4})", text, re.IGNORECASE)
        if match:
            gpu = f"{match.group(1).upper()} {match.group(2)}"
        else:
            gpu = text

        # память
        memory = re.search(r"(\d+)\s*Gb", text, re.IGNORECASE)
        if memory:
            gpu += f" {memory.group(1)}GB"

        return gpu.strip()
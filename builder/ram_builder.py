import re


class RamBuilder:
    """Формирует краткое описание оперативной памяти."""

    def build(self, full_name: str, quantity: int) -> str:

        memory_type = ""
        capacity = ""
        speed = ""

        # Тип памяти
        type_match = re.search(r"(DDR\d)", full_name, re.IGNORECASE)
        if type_match:
            memory_type = type_match.group(1).upper()

        # Объем одного модуля
        cap_match = re.search(r"(\d+)\s*GB", full_name, re.IGNORECASE)
        if cap_match:
            module_size = int(cap_match.group(1))
            capacity = f"{module_size * quantity}GB"
        else:
            module_size = 0

        # Частота
        speed_match = re.search(r"(\d{4,5})\s*MHz", full_name, re.IGNORECASE)
        if speed_match:
            speed = f"{speed_match.group(1)}MHz"

        result = " ".join(
            part for part in (
                memory_type,
                capacity,
                speed,
                f"({quantity}×{module_size})" if quantity > 1 else ""
            )
            if part
        )

        return result
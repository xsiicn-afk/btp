import re


class PsuBuilder:
    """
    Формирует короткое название блока питания.
    """

    def build(self, text: str) -> str:

        # DeepCool PQ1200G 1200W Gen.5 80+ Gold ATX
        text = text.replace("Блок питания", "").strip()

        power = ""

        power_match = re.search(r"(\d{3,4})\s*W", text, re.IGNORECASE)
        if power_match:
            power = f"{power_match.group(1)}W"

        model = text.split()

        if len(model) >= 2:
            result = f"{model[0]} {model[1]}"
        else:
            result = text

        if power:
            result += f" {power}"

        return result.strip()
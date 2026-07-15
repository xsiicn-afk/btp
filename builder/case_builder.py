import re


class CaseBuilder:
    """
    Формирует короткое название корпуса.
    """

    FORM_FACTORS = (
        "E-ATX",
        "ATX",
        "mATX",
        "Micro-ATX",
        "Mini-ITX",
        "ITX",
    )

    def build(self, text: str) -> str:

        text = text.replace("Корпус", "").strip()

        # Убираем хвост после /
        text = text.split("/")[0].strip()

        words = text.split()

        if len(words) >= 2:
            result = f"{words[0]} {' '.join(words[1:4])}"
        else:
            result = text

        form_factor = self.get_form_factor(text)

        if form_factor and form_factor not in result:
            result += f" ({form_factor})"

        return result.strip()

    def get_form_factor(self, text: str) -> str:

        upper = text.upper()

        if "MICRO-ATX" in upper:
            return "mATX"

        if "MINI-ITX" in upper:
            return "Mini-ITX"

        if "E-ATX" in upper:
            return "E-ATX"

        if "MATX" in upper:
            return "mATX"

        if "ATX" in upper:
            return "ATX"

        if "ITX" in upper:
            return "ITX"

        return ""
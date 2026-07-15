from dataclasses import dataclass


@dataclass
class SystemModel:
    """
    Стандартизированное описание модели системного блока.
    """

    series: str = "ByTop PE"

    cpu: str = ""

    ram: str = ""

    storage: str = ""

    gpu: str = ""

    motherboard: str = ""

    cooler: str = ""

    case: str = ""

    psu: str = ""

    def full_name(self) -> str:
        """
        Полное коммерческое название.
        """

        parts = [self.series]

        for value in (
            self.cpu,
            self.ram,
            self.storage,
            self.gpu,
            self.case,
            self.psu,
        ):
            if value:
                parts.append(value)

        return " / ".join(parts)
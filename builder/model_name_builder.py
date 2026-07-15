class ModelNameBuilder:
    """
    Формирует коммерческое название компьютера.
    """

    SERIES = "ByTop PE"

    def build(
        self,
        cpu: str,
        ram: str,
        storage: str,
        gpu: str,
        case: str,
        psu: str,
    ) -> str:

        parts = [self.SERIES]

        if cpu:
            parts.append(cpu)

        if ram:
            short_ram = ram

            # Убираем информацию в скобках
            if "(" in short_ram:
                short_ram = short_ram.split("(")[0].strip()

            words = short_ram.split()

            # DDR5 64GB -> 64GB DDR5
            if len(words) >= 2:
                short_ram = f"{words[1]} {words[0]}"

            parts.append(short_ram)

        if storage:
            parts.append(storage)

        if gpu:
            parts.append(gpu)

        if case:
            parts.append(case)

        if psu:
            parts.append(psu)

        return " / ".join(parts)
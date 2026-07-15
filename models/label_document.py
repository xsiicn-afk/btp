from dataclasses import dataclass, field


@dataclass
class LabelRow:
    """
    Одна строка таблицы спецификации.
    """

    number: int
    name: str
    quantity: int = 1


@dataclass
class LabelDocument:
    """
    Полностью описывает будущую печатную этикетку.

    Один и тот же объект используется:
    - в предпросмотре;
    - при печати;
    - при экспорте PDF.
    """

    # Верхняя часть

    title: str = ""

    serial: str = ""

    article: str = ""

    code: str = ""

    production_date: str = ""

    qr_left: str = ""

    qr_right: str = ""

    # Таблица

    rows: list[LabelRow] = field(default_factory=list)

    # Нижняя часть

    warning: str = (
        "Перед началом эксплуатации прочтите руководство пользователя! "
        "Для обслуживания и ремонта обращайтесь "
        "в авторизованные сервисные центры."
    )

    icons: list[str] = field(default_factory=lambda: [
        "up",
        "electronic",
        "fragile",
        "keep_dry",
    ])
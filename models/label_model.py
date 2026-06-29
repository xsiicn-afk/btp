from dataclasses import dataclass


@dataclass
class LabelModel:
    """Модель данных для отображения и печати этикетки."""

    # Название модели
    title: str = "Системный блок ByTop PE"

    # Основные характеристики
    cpu: str = ""
    motherboard: str = ""
    cooler: str = ""
    ram: str = ""
    storage: str = ""
    gpu: str = ""
    case: str = ""
    psu: str = ""

    # Служебная информация
    serial: str = ""
    article: str = ""
    date: str = ""
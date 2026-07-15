from dataclasses import dataclass, field

from models.additional_item import AdditionalItem
from models.manufacturer import Manufacturer
from models.page_layout import PageLayout


@dataclass
class LabelModel:
    """
    Производственная модель изделия.

    Используется предпросмотром,
    Excel, историей и печатью.
    """

    # -------------------------------------------------
    # Общая информация
    # -------------------------------------------------

    title: str = "Системный блок ЭпикумЛаб"

    model_name: str = ""

    internal_name: str = ""

    manufacturer: Manufacturer = Manufacturer.EPICA

    layout: PageLayout = (
        PageLayout.ONE_SPEC_THREE_ADDRESS
    )

    # -------------------------------------------------
    # Комплектующие
    # -------------------------------------------------

    cpu: str = ""
    motherboard: str = ""
    cooler: str = ""
    ram: str = ""
    storage: str = ""
    gpu: str = ""
    case: str = ""
    psu: str = ""

    # -------------------------------------------------
    # Программное обеспечение
    # -------------------------------------------------

    operating_system: str = ""

    # -------------------------------------------------
    # Дополнительная комплектация
    # -------------------------------------------------

    additional_items: list[AdditionalItem] = field(
        default_factory=list
    )

    # -------------------------------------------------
    # Производство
    # -------------------------------------------------

    serial: str = ""

    article_code: int = 0

    article: str = ""

    date: str = ""
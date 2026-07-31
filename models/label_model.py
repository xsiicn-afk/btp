from dataclasses import dataclass, field

from models.item import Item


@dataclass
class LabelModel:
    """
    Итоговая модель созданного изделия.

    Основным названием модели является model_name.

    Свойства title и internal_name оставлены
    для совместимости со старой системой печати.
    """

    # =====================================================
    # Основные данные изделия
    # =====================================================

    serial: str = ""

    article: str = ""

    article_code: int = 0

    date: str = ""

    # =====================================================
    # Главное название модели
    # =====================================================

    model_name: str = ""

    # =====================================================
    # Гарантия
    # =====================================================

    warranty_months: int = 36

    # =====================================================
    # Основные характеристики
    # =====================================================

    cpu: str = ""

    motherboard: str = ""

    cooler: str = ""

    ram: str = ""

    storage: str = ""

    gpu: str = ""

    case: str = ""

    psu: str = ""

    operating_system: str = ""

    # =====================================================
    # Исходные комплектующие изделия
    # =====================================================

    items: list[Item] = field(
        default_factory=list
    )

    # =====================================================
    # Дополнительные позиции
    # =====================================================

    additional_items: list[Item] = field(
        default_factory=list
    )

    # =====================================================
    # Служебные данные
    # =====================================================

    created_by: str = ""

    version: int = 1

    spec_printed: bool = False

    passport_printed: bool = False

    sticker_printed: bool = False

    # =====================================================
    # Совместимость со старой системой
    # =====================================================

    @property
    def title(self) -> str:

        return self.model_name

    @title.setter
    def title(
        self,
        value: str,
    ):

        self.model_name = (
            value or ""
        )

    # ---------------------------------------------------------

    @property
    def internal_name(self) -> str:

        return self.model_name

    @internal_name.setter
    def internal_name(
        self,
        value: str,
    ):

        self.model_name = (
            value or ""
        )
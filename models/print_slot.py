from dataclasses import dataclass

from models.label_model import LabelModel


@dataclass
class PrintSlot:
    """
    Один блок спецификации
    на листе A4.
    """

    row: int

    column: int

    label: LabelModel
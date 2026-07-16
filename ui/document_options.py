from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QWidget,
)

from models.manufacturer import Manufacturer
from models.page_layout import PageLayout


class DocumentOptions(QWidget):
    """
    Параметры формирования документа.
    """

    changed = Signal()

    def __init__(self):
        super().__init__()

        group = QGroupBox(
            "Документ"
        )

        layout = QFormLayout(group)

        #
        # Производитель
        #

        self.manufacturer = QComboBox()

        self.manufacturer.addItem(
            "ЭпикумЛаб",
            Manufacturer.EPICA,
        )

        self.manufacturer.addItem(
            "Аксус",
            Manufacturer.AXUS,
        )

        #
        # Компоновка листа
        #

        self.layout = QComboBox()

        self.layout.addItem(
            "1 спецификация + 3 адреса",
            PageLayout.ONE_SPEC_THREE_ADDRESS,
        )

        self.layout.addItem(
            "2 спецификации + 2 адреса",
            PageLayout.TWO_SPEC_TWO_ADDRESS,
        )

        self.layout.addItem(
            "3 спецификации + 1 адрес",
            PageLayout.THREE_SPEC_ONE_ADDRESS,
        )

        self.layout.addItem(
            "4 спецификации",
            PageLayout.FOUR_SPEC,
        )

        
        layout.addRow(
            "Производитель:",
            self.manufacturer,
        )

        layout.addRow(
            "Компоновка:",
            self.layout,
        )

        root = QFormLayout(self)

        root.addRow(group)

        #
        # Сигналы
        #

        self.manufacturer.currentIndexChanged.connect(
            self.changed.emit
        )

        self.layout.currentIndexChanged.connect(
            self.changed.emit
        )

    # ---------------------------------------------------------

    def selected_manufacturer(self):

        return self.manufacturer.currentData()

    # ---------------------------------------------------------

    def selected_layout(self):

        return self.layout.currentData()
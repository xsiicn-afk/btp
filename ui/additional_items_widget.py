from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QInputDialog,
)

from models.additional_item import AdditionalItem


class AdditionalItemsWidget(QWidget):
    """
    Виджет дополнительной комплектации.
    """

    changed = Signal()

    def __init__(self):
        super().__init__()

        self._items: list[AdditionalItem] = []

        layout = QVBoxLayout(self)

        self.list = QListWidget()

        layout.addWidget(self.list)

        buttons = QHBoxLayout()

        self.add_button = QPushButton(
            "➕ Добавить"
        )

        self.remove_button = QPushButton(
            "➖ Удалить"
        )

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.remove_button)

        layout.addLayout(buttons)

        self.add_button.clicked.connect(
            self.add_item
        )

        self.remove_button.clicked.connect(
            self.remove_item
        )

    # -------------------------------------------------

    def set_items(
        self,
        items: list[AdditionalItem],
    ):

        self._items = list(items)

        self.refresh()

    # -------------------------------------------------

    def items(self):

        return list(self._items)

    # -------------------------------------------------

    def refresh(self):

        self.list.clear()

        for item in self._items:

            self.list.addItem(
                f"{item.name}   ×{item.quantity}"
            )

    # -------------------------------------------------

    def add_item(self):

        text, ok = QInputDialog.getText(
            self,
            "Дополнительная комплектация",
            "Название:",
        )

        if not ok:
            return

        text = text.strip()

        if not text:
            return

        self._items.append(
            AdditionalItem(
                name=text,
                quantity=1,
            )
        )

        self.refresh()

        self.changed.emit()

    # -------------------------------------------------

    def remove_item(self):

        row = self.list.currentRow()

        if row < 0:
            return

        del self._items[row]

        self.refresh()

        self.changed.emit()
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from models.configuration import Configuration


class ComponentsTable(QTableWidget):
    """Таблица комплектующих."""

    def __init__(self):
        super().__init__()

        self.setColumnCount(3)

        self.setHorizontalHeaderLabels([
            "Категория",
            "Наименование",
            "Количество",
        ])

        self.horizontalHeader().setStretchLastSection(False)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.setColumnWidth(0, 140)
        self.setColumnWidth(2, 90)

    def set_data(self, configuration: Configuration):

        self.setRowCount(0)

        for item in configuration.items:

            row = self.rowCount()
            self.insertRow(row)

            self.setItem(
                row,
                0,
                QTableWidgetItem(item.category.value)
            )

            self.setItem(
                row,
                1,
                QTableWidgetItem(item.name)
            )

            self.setItem(
                row,
                2,
                QTableWidgetItem(str(item.quantity))
            )
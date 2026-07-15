from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
)

from services.build_history_service import BuildHistoryService


class HistoryPanel(QWidget):

    build_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self.history = BuildHistoryService()

        layout = QVBoxLayout(self)

        #
        # Поиск
        #

        top = QHBoxLayout()

        top.addWidget(QLabel("Поиск:"))

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Введите S/N или модель..."
        )

        top.addWidget(self.search)

        layout.addLayout(top)

        #
        # Таблица
        #

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            [
                "S/N",
                "Дата",
                "Модель",
            ]
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(self.table)

        self.table.doubleClicked.connect(
            self.double_clicked
        )

        self.search.textChanged.connect(
            self.filter
        )

        self.rows = []

        self.refresh()

    # ---------------------------------------------------------

    def refresh(self):

        self.rows = self.history.all()

        self.show_rows(self.rows)

    # ---------------------------------------------------------

    def show_rows(self, rows):

        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):

            self.table.setItem(
                r,
                0,
                QTableWidgetItem(
                    str(row["serial"])
                ),
            )

            self.table.setItem(
                r,
                1,
                QTableWidgetItem(
                    row["build_date"]
                ),
            )

            self.table.setItem(
                r,
                2,
                QTableWidgetItem(
                    row["title"]
                ),
            )

        self.table.resizeColumnsToContents()

    # ---------------------------------------------------------

    def filter(self, text):

        text = text.lower()

        rows = []

        for row in self.rows:

            if (
                text in str(row["serial"]).lower()
                or text in row["title"].lower()
            ):

                rows.append(row)

        self.show_rows(rows)

    # ---------------------------------------------------------

    def double_clicked(self):

        row = self.table.currentRow()

        if row < 0:
            return

        serial = self.table.item(
            row,
            0,
        ).text()

        self.build_selected.emit(serial)
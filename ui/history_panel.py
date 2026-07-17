from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)

from services.build_history_service import BuildHistoryService


class HistoryPanel(QWidget):

    build_selected = Signal(str)

    specification_requested = Signal(list)

    passport_requested = Signal(list)

    sticker_requested = Signal(list)

    refresh_requested = Signal()

    def __init__(self):
        super().__init__()

        self.history = BuildHistoryService()

        self.rows = []

        root = QVBoxLayout(self)

        #
        # Верхняя панель
        #

        top = QHBoxLayout()

        top.addWidget(QLabel("Поиск"))

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "S/N, модель, пользователь..."
        )

        top.addWidget(self.search)

        self.refresh_button = QPushButton(
            "Обновить"
        )

        top.addWidget(self.refresh_button)

        root.addLayout(top)

        #
        # Таблица
        #

        self.table = QTableWidget()

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels(
            [
                "",
                "S/N",
                "Дата",
                "Модель",
                "Создал",
                "Спец.",
                "Паспорт",
                "Стикер",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().hide()

        root.addWidget(self.table)

        #
        # Нижняя панель
        #

        bottom = QHBoxLayout()

        self.spec_button = QPushButton(
            "Печать спецификации"
        )

        self.passport_button = QPushButton(
            "Печать паспорта"
        )

        self.sticker_button = QPushButton(
            "Печать стикеров"
        )

        bottom.addWidget(self.spec_button)
        bottom.addWidget(self.passport_button)
        bottom.addWidget(self.sticker_button)

        root.addLayout(bottom)

        #
        # Сигналы
        #

        self.search.textChanged.connect(
            self.filter
        )

        self.refresh_button.clicked.connect(
            self.refresh
        )

        self.table.doubleClicked.connect(
            self.double_clicked
        )

        self.spec_button.clicked.connect(
            self.print_specifications
        )

        self.passport_button.clicked.connect(
            self.print_passports
        )

        self.sticker_button.clicked.connect(
            self.print_stickers
        )

        self.refresh()

    # ---------------------------------------------------------

    def refresh(self):

        self.rows = self.history.all()

        self.show_rows(self.rows)

    # ---------------------------------------------------------

    def show_rows(self, rows):

        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):

            check = QTableWidgetItem()

            check.setFlags(
                Qt.ItemIsEnabled
                | Qt.ItemIsSelectable
                | Qt.ItemIsUserCheckable
            )

            check.setCheckState(Qt.Unchecked)

            self.table.setItem(r, 0, check)

            self.table.setItem(
                r,
                1,
                QTableWidgetItem(
                    str(row["serial"])
                ),
            )

            self.table.setItem(
                r,
                2,
                QTableWidgetItem(
                    str(row["build_date"])
                ),
            )

            self.table.setItem(
                r,
                3,
                QTableWidgetItem(
                    str(row["title"])
                ),
            )

            created_by = ""

            if "created_by" in row.keys():

                created_by = row["created_by"] or ""

            self.table.setItem(
                r,
                4,
                QTableWidgetItem(
                    str(created_by)
                ),
            )

            spec = ""

            if (
                "spec_printed" in row.keys()
                and row["spec_printed"]
            ):
                spec = "✓"

            passport = ""

            if (
                "passport_printed" in row.keys()
                and row["passport_printed"]
            ):
                passport = "✓"

            sticker = ""

            if (
                "sticker_printed" in row.keys()
                and row["sticker_printed"]
            ):
                sticker = "✓"

            self.table.setItem(
                r,
                5,
                QTableWidgetItem(spec),
            )

            self.table.setItem(
                r,
                6,
                QTableWidgetItem(passport),
            )

            self.table.setItem(
                r,
                7,
                QTableWidgetItem(sticker),
            )

        self.table.resizeColumnsToContents()
    # ---------------------------------------------------------

    def filter(self, text):

        text = text.lower().strip()

        if not text:

            self.show_rows(self.rows)

            return

        result = []

        for row in self.rows:

            serial = str(
                row["serial"]
            ).lower()

            title = str(
                row["title"]
            ).lower()

            if "created_by" in row.keys():

                created = str(
                    row["created_by"] or ""
                ).lower()

            else:

                created = ""

            if (
                text in serial
                or text in title
                or text in created
            ):

                result.append(row)

        self.show_rows(result)

    # ---------------------------------------------------------

    def selected_serials(self):

        result = []

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0,
            )

            if (
                item is not None
                and item.checkState() == Qt.Checked
            ):

                result.append(

                    self.table.item(
                        row,
                        1,
                    ).text()

                )

        return result

    # ---------------------------------------------------------

    def current_serial(self):

        row = self.table.currentRow()

        if row < 0:

            return None

        return self.table.item(
            row,
            1,
        ).text()

    # ---------------------------------------------------------

    def double_clicked(self):

        serial = self.current_serial()

        if serial:

            self.build_selected.emit(
                serial
            )

    # ---------------------------------------------------------

    def print_specifications(self):

        serials = self.selected_serials()

        if not serials:

            serial = self.current_serial()

            if serial:

                serials.append(serial)

        if serials:

            self.specification_requested.emit(
                serials
            )

    # ---------------------------------------------------------

    def print_passports(self):

        serials = self.selected_serials()

        if not serials:

            serial = self.current_serial()

            if serial:

                serials.append(serial)

        if serials:

            self.passport_requested.emit(
                serials
            )

    # ---------------------------------------------------------

    def print_stickers(self):

        serials = self.selected_serials()

        if not serials:

            serial = self.current_serial()

            if serial:

                serials.append(serial)

        if serials:

            self.sticker_requested.emit(
                serials
            )

    # ---------------------------------------------------------

    def select_all(self):

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0,
            )

            if item:

                item.setCheckState(
                    Qt.Checked
                )

    # ---------------------------------------------------------

    def clear_selection(self):

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0,
            )

            if item:

                item.setCheckState(
                    Qt.Unchecked
                )

    # ---------------------------------------------------------

    def invert_selection(self):

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0,
            )

            if item is None:

                continue

            if item.checkState() == Qt.Checked:

                item.setCheckState(
                    Qt.Unchecked
                )

            else:

                item.setCheckState(
                    Qt.Checked
                )
    # ---------------------------------------------------------

    def selected_count(self):

        return len(
            self.selected_serials()
        )

    # ---------------------------------------------------------

    def has_selection(self):

        return (
            self.selected_count() > 0
        )

    # ---------------------------------------------------------

    def selected_rows(self):

        rows = []

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0,
            )

            if (
                item is not None
                and item.checkState() == Qt.Checked
            ):

                rows.append(row)

        return rows

    # ---------------------------------------------------------

    def update_print_status(
        self,
        serials,
        column,
    ):

        serials = {
            str(serial)
            for serial in serials
        }

        for row in range(
            self.table.rowCount()
        ):

            serial = self.table.item(
                row,
                1,
            ).text()

            if serial in serials:

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem("✓"),
                )

    # ---------------------------------------------------------

    def mark_specification_printed(
        self,
        serials,
    ):

        self.update_print_status(
            serials,
            5,
        )

    # ---------------------------------------------------------

    def mark_passport_printed(
        self,
        serials,
    ):

        self.update_print_status(
            serials,
            6,
        )

    # ---------------------------------------------------------

    def mark_sticker_printed(
        self,
        serials,
    ):

        self.update_print_status(
            serials,
            7,
        )

    # ---------------------------------------------------------

    def clear(self):

        self.rows = []

        self.table.setRowCount(0)

        self.search.clear()

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from printing.print_engine import PrintEngine


class SpecificationPrintDialog(QDialog):

    def __init__(
        self,
        labels_count: int,
        parent=None,
    ):
        super().__init__(parent)

        self.labels_count = labels_count

        self.setWindowTitle(
            "Печать спецификаций"
        )

        self.setFixedWidth(360)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.labels_label = QLabel(
            str(labels_count)
        )

        form.addRow(
            "Спецификаций к печати",
            self.labels_label,
        )

        self.position = QComboBox()

        for i in range(1, 5):
            self.position.addItem(str(i), i)

        self.position.currentIndexChanged.connect(
            self.update_sheet_count
        )

        form.addRow(
            "Начинать с позиции",
            self.position,
        )

        self.sheets_label = QLabel()

        form.addRow(
            "Листов будет напечатано",
            self.sheets_label,
        )

        layout.addLayout(form)

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.ok = QPushButton(
            "Печатать"
        )

        self.cancel = QPushButton(
            "Отмена"
        )

        self.ok.clicked.connect(
            self.accept
        )

        self.cancel.clicked.connect(
            self.reject
        )

        buttons.addWidget(self.ok)
        buttons.addWidget(self.cancel)

        layout.addLayout(buttons)

        self.update_sheet_count()

    # ---------------------------------------------------------

    def update_sheet_count(self):

        pages = PrintEngine.pages_required(
            self.labels_count,
            self.first_position(),
        )

        self.sheets_label.setText(
            str(pages)
        )

    # ---------------------------------------------------------

    def first_position(self) -> int:

        return self.position.currentData()

    # ---------------------------------------------------------

    def sheet_count(self) -> int:

        return PrintEngine.pages_required(
            self.labels_count,
            self.first_position(),
        )
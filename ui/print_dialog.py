from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

from models.page_layout import PageLayout


class PrintDialog(QDialog):
    """
    Диалог параметров печати.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Печать")
        self.setFixedWidth(420)

        root = QVBoxLayout(self)

        form = QFormLayout()

        #
        # Количество экземпляров
        #

        self.count = QComboBox()

        self.count.addItems(
            [
                "1",
                "2",
                "3",
                "4",
            ]
        )

        form.addRow(
            "Количество компьютеров:",
            self.count,
        )

        #
        # Компоновка листа
        #

        

        root.addLayout(form)

        buttons = QHBoxLayout()

        self.print_button = QPushButton(
            "Печатать"
        )

        self.cancel_button = QPushButton(
            "Отмена"
        )

        self.print_button.clicked.connect(
            self.accept
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        buttons.addWidget(
            self.print_button
        )

        buttons.addWidget(
            self.cancel_button
        )

        root.addLayout(buttons)

    # ---------------------------------------------------------

    def copies(self) -> int:

        return int(
            self.count.currentText()
        )

    # ---------------------------------------------------------

    def page_layout(self):

        layout = self.layout.currentData()

        if layout is not None:
            return layout

        count = self.copies()

        if count == 1:
            return PageLayout.ONE_SPEC_THREE_ADDRESS

        if count == 2:
            return PageLayout.TWO_SPEC_TWO_ADDRESS

        if count == 3:
            return PageLayout.THREE_SPEC_ONE_ADDRESS

        return PageLayout.FOUR_SPEC
    # ---------------------------------------------------------

    def start_position(self) -> int:

        return int(
            self.first_position.currentText()
        )
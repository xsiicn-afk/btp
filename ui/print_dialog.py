from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)


class PrintDialog(QDialog):
    """
    Диалог выбора позиции печати на листе A4.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Печать спецификации")
        self.setFixedWidth(320)

        layout = QVBoxLayout(self)

        title = QLabel("Выберите позицию на листе A4:")
        layout.addWidget(title)

        self.group = QButtonGroup(self)

        self.r1 = QRadioButton("1 — верхняя левая")
        self.r2 = QRadioButton("2 — верхняя правая")
        self.r3 = QRadioButton("3 — нижняя левая")
        self.r4 = QRadioButton("4 — нижняя правая")

        self.group.addButton(self.r1, 1)
        self.group.addButton(self.r2, 2)
        self.group.addButton(self.r3, 3)
        self.group.addButton(self.r4, 4)

        self.r1.setChecked(True)

        layout.addWidget(self.r1)
        layout.addWidget(self.r2)
        layout.addWidget(self.r3)
        layout.addWidget(self.r4)

        self.print_button = QPushButton("Печатать")
        self.cancel_button = QPushButton("Отмена")

        self.print_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.print_button)
        layout.addWidget(self.cancel_button)

    def get_position(self) -> int:
        """
        Возвращает выбранную позицию (1–4).
        """
        return self.group.checkedId()
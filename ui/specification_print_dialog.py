from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class SpecificationPrintDialog(QDialog):
    """
    Диалог печати спецификации.

    Новая схема:
        одно изделие = одна этикетка 100×150.
    """

    def __init__(
        self,
        labels_count: int,
        parent=None,
    ):
        super().__init__(parent)

        self.labels_count = labels_count

        self.setWindowTitle("Печать спецификаций")
        self.setFixedWidth(360)

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel(
                f"Будет распечатано спецификаций: {labels_count}"
            )
        )

        layout.addWidget(
            QLabel(
                "Формат: 100×150 мм"
            )
        )

        layout.addStretch()

        buttons = QHBoxLayout()

        buttons.addStretch()

        ok = QPushButton("Печатать")
        cancel = QPushButton("Отмена")

        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

        buttons.addWidget(ok)
        buttons.addWidget(cancel)

        layout.addLayout(buttons)
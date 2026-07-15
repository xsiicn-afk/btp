from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from models.label_model import LabelModel


class PreviewWidget(QWidget):
    """
    Временный виджет предпросмотра.

    До завершения перехода на Excel COM
    QPainter больше не используется.

    Позже здесь будет отображаться
    настоящий PDF, сформированный Excel.
    """

    def __init__(self):
        super().__init__()

        self.label = LabelModel()

        layout = QVBoxLayout(self)

        info = QLabel(
            "Предпросмотр временно отключён.\n\n"
            "Документ формируется\n"
            "непосредственно в Microsoft Excel.\n\n"
            "После завершения формирования\n"
            "здесь будет отображаться\n"
            "готовый PDF."
        )

        info.setAlignment(Qt.AlignCenter)

        info.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(info)
        layout.addStretch()

    # ---------------------------------------------------------

    def set_label(self, label: LabelModel):

        self.label = label
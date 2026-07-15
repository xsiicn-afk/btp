from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QFrame

from models.label_model import LabelModel
from ui.base_section_widget import BaseSectionWidget


class FooterWidget(BaseSectionWidget):
    """
    Нижняя часть этикетки.
    """

    def __init__(self):
        super().__init__()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        self.layout.addWidget(line)

        self.article = QLabel()
        self.serial = QLabel()
        self.date = QLabel()

        for widget in (
            self.article,
            self.serial,
            self.date,
        ):
            widget.setStyleSheet("""
                font-size:11px;
            """)
            self.layout.addWidget(widget)

        icons = QLabel("↑    ☂    ⌂    ♻")
        icons.setAlignment(Qt.AlignCenter)
        icons.setStyleSheet("""
            font-size:20px;
            padding-top:8px;
        """)

        self.layout.addWidget(icons)

    def set_label(self, model: LabelModel):

        self.article.setText(f"Артикул: {model.article or '—'}")
        self.serial.setText(f"Серийный №: {model.serial or '—'}")
        self.date.setText(f"Дата изготовления: {model.date or '—'}")
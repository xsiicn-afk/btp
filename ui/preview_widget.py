from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from models.label_model import LabelModel


class PreviewWidget(QWidget):
    """Предпросмотр этикетки."""

    def __init__(self):
        super().__init__()

        outer_layout = QVBoxLayout(self)

        # Лист бумаги
        self.paper = QWidget()
        self.paper.setFixedSize(400, 580)

        self.paper.setStyleSheet("""
            QWidget{
                background:white;
                border:2px solid black;
                border-radius:4px;
            }
        """)

        layout = QVBoxLayout(self.paper)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Название модели
        self.title = QLabel("Системный блок ByTop PE")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setWordWrap(True)
        self.title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(self.title)

        # Конфигурация

        self.cpu = QLabel()
        self.ram = QLabel()
        self.storage = QLabel()
        self.gpu = QLabel()
        self.case = QLabel()
        self.psu = QLabel()

        for widget in (
            self.cpu,
            self.ram,
            self.storage,
            self.gpu,
            self.case,
            self.psu,
        ):
            widget.setWordWrap(True)
            widget.setStyleSheet("font-size:13px;")
            layout.addWidget(widget)

        layout.addStretch()

        self.article = QLabel()
        self.serial = QLabel()
        self.date = QLabel()

        self.article.setStyleSheet("font-size:12px;")
        self.serial.setStyleSheet("font-size:12px;")
        self.date.setStyleSheet("font-size:12px;")

        layout.addWidget(self.article)
        layout.addWidget(self.serial)
        layout.addWidget(self.date)

        outer_layout.addWidget(self.paper, alignment=Qt.AlignCenter)

    def set_label(self, model: LabelModel):

        self.title.setText(model.title)

        self.cpu.setText(model.cpu)
        self.ram.setText(model.ram)
        self.storage.setText(model.storage)
        self.gpu.setText(model.gpu)
        self.case.setText(model.case)
        self.psu.setText(model.psu)

        self.article.setText(f"Артикул: {model.article or '—'}")
        self.serial.setText(f"Серийный №: {model.serial or '—'}")
        self.date.setText(f"Дата: {model.date or '—'}")
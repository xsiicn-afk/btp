from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from models.label_model import LabelModel


class BuildCard(QWidget):

    pdf_requested = Signal()
    print_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        #
        # Заголовок
        #

        self.title = QLabel()
        self.title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )
        layout.addWidget(self.title)

        self.model = QLabel()
        self.model.setWordWrap(True)
        layout.addWidget(self.model)

        layout.addSpacing(15)

        #
        # Общая информация
        #

        self.serial = QLabel()
        self.article = QLabel()
        self.date = QLabel()

        layout.addWidget(self.serial)
        layout.addWidget(self.article)
        layout.addWidget(self.date)

        layout.addSpacing(15)

        #
        # Комплектующие
        #

        self.cpu = QLabel()
        self.board = QLabel()
        self.cooler = QLabel()
        self.ram = QLabel()
        self.storage = QLabel()
        self.gpu = QLabel()
        self.case = QLabel()
        self.psu = QLabel()

        for widget in (
            self.cpu,
            self.board,
            self.cooler,
            self.ram,
            self.storage,
            self.gpu,
            self.case,
            self.psu,
        ):
            widget.setWordWrap(True)
            widget.setFrameShape(QFrame.Box)
            widget.setMargin(6)
            layout.addWidget(widget)

        layout.addStretch()

        #
        # Кнопки
        #

        buttons = QHBoxLayout()

        self.pdf_button = QPushButton("PDF")
        self.print_button = QPushButton("Печать")

        buttons.addWidget(self.pdf_button)
        buttons.addWidget(self.print_button)

        layout.addLayout(buttons)

        self.pdf_button.clicked.connect(
            self.pdf_requested.emit
        )

        self.print_button.clicked.connect(
            self.print_requested.emit
        )

    # ---------------------------------------------------------

    def set_label(
        self,
        label: LabelModel,
    ):

        self.title.setText(label.title)
        self.model.setText(label.model_name)

        self.serial.setText(f"S/N: {label.serial}")
        self.article.setText(f"Артикул: {label.article_code}")
        self.date.setText(f"Дата: {label.date}")

        self.cpu.setText(f"CPU\n\n{label.cpu or '—'}")

        self.board.setText(
            f"Материнская плата\n\n{label.motherboard or '—'}"
        )

        self.cooler.setText(
            f"Охлаждение\n\n{label.cooler or '—'}"
        )

        self.ram.setText(
            f"RAM\n\n{label.ram or '—'}"
        )

        self.storage.setText(
            f"SSD / HDD\n\n{label.storage or '—'}"
        )

        self.gpu.setText(
            f"Видео\n\n{label.gpu or '—'}"
        )

        self.case.setText(
            f"Корпус\n\n{label.case or '—'}"
        )

        self.psu.setText(
            f"Блок питания\n\n{label.psu or '—'}"
        )
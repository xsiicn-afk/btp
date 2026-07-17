from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)

from models.label_model import LabelModel


class BuildCard(QWidget):

    save_requested = Signal()
    specification_requested = Signal()
    passport_requested = Signal()
    sticker_requested = Signal()

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        #
        # Заголовок
        #

        self.title = QLabel()
        self.title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        self.model = QLabel()
        self.model.setWordWrap(True)

        root.addWidget(self.title)
        root.addWidget(self.model)

        #
        # Общая информация
        #

        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Box)

        info_layout = QGridLayout(info_frame)

        self.serial = QLabel()

        self.article = QLabel()

        self.date = QLabel()

        self.created_by = QLabel()

        self.version = QLabel()

        info_layout.addWidget(QLabel("Серийный номер"), 0, 0)
        info_layout.addWidget(self.serial, 0, 1)

        info_layout.addWidget(QLabel("Артикул"), 1, 0)
        info_layout.addWidget(self.article, 1, 1)

        info_layout.addWidget(QLabel("Дата"), 2, 0)
        info_layout.addWidget(self.date, 2, 1)

        info_layout.addWidget(QLabel("Создал"), 3, 0)
        info_layout.addWidget(self.created_by, 3, 1)

        info_layout.addWidget(QLabel("Версия"), 4, 0)
        info_layout.addWidget(self.version, 4, 1)

        root.addWidget(info_frame)

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

        self.component_widgets = [
            ("Процессор", self.cpu),
            ("Материнская плата", self.board),
            ("Охлаждение", self.cooler),
            ("Оперативная память", self.ram),
            ("Накопители", self.storage),
            ("Видеоадаптер", self.gpu),
            ("Корпус", self.case),
            ("Блок питания", self.psu),
        ]

        for title, widget in self.component_widgets:

            frame = QFrame()
            frame.setFrameShape(QFrame.Box)

            layout = QVBoxLayout(frame)

            caption = QLabel(title)
            caption.setStyleSheet("font-weight:bold;")

            widget.setWordWrap(True)

            layout.addWidget(caption)
            layout.addWidget(widget)

            root.addWidget(frame)
        #
        # Статус
        #

        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.Box)

        status_layout = QVBoxLayout(status_frame)

        title = QLabel("Статус изделия")
        title.setStyleSheet("font-weight:bold;")

        status_layout.addWidget(title)

        self.status = QLabel("Создано")

        self.specification_status = QLabel("Спецификация: не печаталась")
        self.passport_status = QLabel("Паспорт: не печатался")
        self.sticker_status = QLabel("Стикер: не печатался")

        status_layout.addWidget(self.status)
        status_layout.addWidget(self.specification_status)
        status_layout.addWidget(self.passport_status)
        status_layout.addWidget(self.sticker_status)

        root.addWidget(status_frame)

        root.addStretch()

        #
        # Кнопки
        #

        buttons = QHBoxLayout()

        self.save_button = QPushButton(
            "Сохранить"
        )

        self.specification_button = QPushButton(
            "Печать спецификации"
        )

        self.passport_button = QPushButton(
            "Печать паспорта"
        )

        self.sticker_button = QPushButton(
            "Печать стикера"
        )

        buttons.addWidget(self.save_button)
        buttons.addWidget(self.specification_button)
        buttons.addWidget(self.passport_button)
        buttons.addWidget(self.sticker_button)

        root.addLayout(buttons)

        #
        # Сигналы
        #

        self.save_button.clicked.connect(
            self.save_requested.emit
        )

        self.specification_button.clicked.connect(
            self.specification_requested.emit
        )

        self.passport_button.clicked.connect(
            self.passport_requested.emit
        )

        self.sticker_button.clicked.connect(
            self.sticker_requested.emit
        )
    # ---------------------------------------------------------

    def set_label(
        self,
        label: LabelModel,
    ):

        #
        # Заголовок
        #

        self.title.setText(
            label.title or ""
        )

        self.model.setText(
            label.model_name or ""
        )

        #
        # Общая информация
        #

        self.serial.setText(
            label.serial or "—"
        )

        self.article.setText(
            str(label.article_code or "")
        )

        self.date.setText(
            label.date or "—"
        )

        self.created_by.setText(
            getattr(
                label,
                "created_by",
                ""
            ) or "—"
        )

        self.version.setText(
            str(
                getattr(
                    label,
                    "version",
                    1,
                )
            )
        )

        #
        # Комплектующие
        #

        self.cpu.setText(
            label.cpu or "—"
        )

        self.board.setText(
            label.motherboard or "—"
        )

        self.cooler.setText(
            label.cooler or "—"
        )

        self.ram.setText(
            label.ram or "—"
        )

        self.storage.setText(
            label.storage or "—"
        )

        self.gpu.setText(
            label.gpu or "—"
        )

        self.case.setText(
            label.case or "—"
        )

        self.psu.setText(
            label.psu or "—"
        )

        #
        # Статус
        #

        self.status.setText(
            getattr(
                label,
                "status",
                "Создано",
            )
        )

        if getattr(
            label,
            "spec_printed",
            False,
        ):

            self.specification_status.setText(
                "Спецификация: напечатана"
            )

        else:

            self.specification_status.setText(
                "Спецификация: не печаталась"
            )

        if getattr(
            label,
            "passport_printed",
            False,
        ):

            self.passport_status.setText(
                "Паспорт: напечатан"
            )

        else:

            self.passport_status.setText(
                "Паспорт: не печатался"
            )

        if getattr(
            label,
            "sticker_printed",
            False,
        ):

            self.sticker_status.setText(
                "Стикер: напечатан"
            )

        else:

            self.sticker_status.setText(
                "Стикер: не печатался"
            )
    # ---------------------------------------------------------

    def set_status(
        self,
        text: str,
    ):

        self.status.setText(text)

    # ---------------------------------------------------------

    def set_specification_printed(
        self,
        printed: bool,
    ):

        if printed:

            self.specification_status.setText(
                "Спецификация: напечатана"
            )

        else:

            self.specification_status.setText(
                "Спецификация: не печаталась"
            )

    # ---------------------------------------------------------

    def set_passport_printed(
        self,
        printed: bool,
    ):

        if printed:

            self.passport_status.setText(
                "Паспорт: напечатан"
            )

        else:

            self.passport_status.setText(
                "Паспорт: не печатался"
            )

    # ---------------------------------------------------------

    def set_sticker_printed(
        self,
        printed: bool,
    ):

        if printed:

            self.sticker_status.setText(
                "Стикер: напечатан"
            )

        else:

            self.sticker_status.setText(
                "Стикер: не печатался"
            )

    # ---------------------------------------------------------

    def lock(self):

        self.save_button.setEnabled(False)

    # ---------------------------------------------------------

    def unlock(self):

        self.save_button.setEnabled(True)

    # ---------------------------------------------------------

    def set_print_enabled(
        self,
        enabled: bool,
    ):

        self.specification_button.setEnabled(enabled)

        self.passport_button.setEnabled(enabled)

        self.sticker_button.setEnabled(enabled)
    # ---------------------------------------------------------

    def clear(self):

        empty = LabelModel()

        self.set_label(empty)

    # ---------------------------------------------------------

    def current_serial(self) -> str:

        return self.serial.text()

    # ---------------------------------------------------------

    def current_article(self) -> str:

        return self.article.text()

    # ---------------------------------------------------------

    def current_title(self) -> str:

        return self.title.text()

    # ---------------------------------------------------------

    def current_model(self) -> str:

        return self.model.text()

    # ---------------------------------------------------------

    def update_version(
        self,
        version: int,
    ):

        self.version.setText(
            str(version)
        )

    # ---------------------------------------------------------

    def update_creator(
        self,
        creator: str,
    ):

        self.created_by.setText(
            creator or "—"
        )

    # ---------------------------------------------------------

    def update_date(
        self,
        date: str,
    ):

        self.date.setText(
            date or "—"
        )
    # ---------------------------------------------------------

    def clear(self):

        empty = LabelModel()

        self.set_label(empty)

    # ---------------------------------------------------------

    def current_serial(self) -> str:

        return self.serial.text()

    # ---------------------------------------------------------

    def current_article(self) -> str:

        return self.article.text()

    # ---------------------------------------------------------

    def current_title(self) -> str:

        return self.title.text()

    # ---------------------------------------------------------

    def current_model(self) -> str:

        return self.model.text()

    # ---------------------------------------------------------

    def update_version(
        self,
        version: int,
    ):

        self.version.setText(
            str(version)
        )

    # ---------------------------------------------------------

    def update_creator(
        self,
        creator: str,
    ):

        self.created_by.setText(
            creator or "—"
        )

    # ---------------------------------------------------------

    def update_date(
        self,
        date: str,
    ):

        self.date.setText(
            date or "—"
        )            
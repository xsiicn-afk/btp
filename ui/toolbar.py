from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
)


class MainToolBar(QWidget):

    paste_requested = Signal()
    new_build_requested = Signal()
    history_requested = Signal()
    settings_requested = Signal()

    def __init__(self):
        super().__init__()

        self.init_ui()

    # ---------------------------------------------------------

    def init_ui(self):

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            6
        )

        # -------------------------------------------------
        # Кнопки
        # -------------------------------------------------

        self.btn_paste = QPushButton(
            "Обновить"
        )

        self.btn_new_build = QPushButton(
            "Создать изделие"
        )

        self.btn_history = QPushButton(
            "История"
        )

        self.btn_settings = QPushButton(
            "Настройки"
        )

        # -------------------------------------------------
        # Все кнопки располагаются подряд слева.
        # -------------------------------------------------

        layout.addWidget(
            self.btn_paste
        )

        layout.addWidget(
            self.btn_new_build
        )

        layout.addWidget(
            self.btn_history
        )

        layout.addWidget(
            self.btn_settings
        )

        # Свободное место остаётся справа.

        layout.addStretch()

        # -------------------------------------------------
        # Сигналы
        # -------------------------------------------------

        self.btn_paste.clicked.connect(
            self.paste_requested.emit
        )

        self.btn_new_build.clicked.connect(
            self.new_build_requested.emit
        )

        self.btn_history.clicked.connect(
            self.history_requested.emit
        )

        self.btn_settings.clicked.connect(
            self.settings_requested.emit
        )
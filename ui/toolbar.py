from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar


class MainToolBar(QToolBar):

    paste_requested = Signal()
    new_build_requested = Signal()

    export_pdf_requested = Signal()

    print_requested = Signal()
    history_requested = Signal()
    settings_requested = Signal()

    def __init__(self):
        super().__init__("Инструменты")

        self.setMovable(False)

        #
        # Вставить
        #

        action = QAction("📋 Вставить", self)
        action.triggered.connect(
            self.paste_requested.emit
        )
        self.addAction(action)

        #
        # Создать документ
        #

        action = QAction("🆕 Создать документ", self)
        action.triggered.connect(
            self.new_build_requested.emit
        )
        self.addAction(action)

        self.addSeparator()

        #
        # Документ
        #

        action = QAction("📄 Документ", self)
        action.triggered.connect(
            self.export_pdf_requested.emit
        )
        self.addAction(action)

        #
        # Печать
        #

        action = QAction("🖨 Печать", self)
        action.triggered.connect(
            self.print_requested.emit
        )
        self.addAction(action)

        self.addSeparator()

        #
        # История
        #

        action = QAction("📚 История", self)
        action.triggered.connect(
            self.history_requested.emit
        )
        self.addAction(action)

        self.addSeparator()

        #
        # Настройки
        #

        action = QAction("⚙ Настройки", self)
        action.triggered.connect(
            self.settings_requested.emit
        )
        self.addAction(action)
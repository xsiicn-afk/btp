from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar


class MainToolBar(QToolBar):
    paste_requested = Signal()

    def __init__(self):
        super().__init__("Инструменты")

        self.setMovable(False)

        paste_action = QAction("📋 Вставить из буфера", self)
        paste_action.triggered.connect(self.paste_requested.emit)

        self.addAction(paste_action)
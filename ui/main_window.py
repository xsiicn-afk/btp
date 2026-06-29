from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QSplitter,
    QWidget,
)

from builder.model_builder import ModelBuilder
from parser.basic_parser import BasicParser

from ui.clipboard_panel import ClipboardPanel
from ui.components_table import ComponentsTable
from ui.menu import create_menu
from ui.preview_widget import PreviewWidget
from ui.statusbar import MainStatusBar
from ui.toolbar import MainToolBar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ByTop Production Suite")
        self.resize(1500, 900)

        # Логика
        self.parser = BasicParser()
        self.model_builder = ModelBuilder()

        # UI
        self.clipboard_panel = ClipboardPanel()
        self.components_table = ComponentsTable()
        self.preview_widget = PreviewWidget()

        self.init_ui()

    def init_ui(self):

        create_menu(self)

        self.toolbar = MainToolBar()
        self.addToolBar(self.toolbar)

        self.toolbar.paste_requested.connect(self.paste_from_clipboard)

        self.setStatusBar(MainStatusBar())

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(self.clipboard_panel)
        splitter.addWidget(self.components_table)
        splitter.addWidget(self.preview_widget)

        splitter.setSizes([600, 700, 300])

        self.clipboard_panel.setMinimumWidth(300)
        self.components_table.setMinimumWidth(300)
        self.preview_widget.setMinimumWidth(250)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 4)
        splitter.setStretchFactor(2, 2)

        layout.addWidget(splitter)

    def paste_from_clipboard(self):

        clipboard = QApplication.clipboard()
        text = clipboard.text()

        self.clipboard_panel.setPlainText(text)

        configuration = self.parser.parse(text)

        configuration.serial = datetime.now().strftime("%d%m") + "001"
        configuration.date = datetime.now().strftime("%d.%m.%Y")

        self.components_table.set_data(configuration)

        label = self.model_builder.build(configuration)

        self.preview_widget.set_label(label)
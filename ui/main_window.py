from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QWidget,
)

from parser.basic_parser import BasicParser

from models.configuration import Configuration
from models.label_model import LabelModel

from printing.print_engine import PrintEngine

from services.build_service import BuildService

from ui.clipboard_panel import ClipboardPanel
from ui.components_table import ComponentsTable
from ui.preview_panel import PreviewPanel
from ui.toolbar import MainToolBar
from ui.print_dialog import PrintDialog
from ui.settings_dialog import SettingsDialog
from ui.history_window import HistoryWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #
        # Сервисы
        #

        self.parser = BasicParser()

        self.build_service = BuildService()

        self.print_engine = PrintEngine()

        #
        # Данные
        #

        self.current_configuration = Configuration()

        self.current_label = LabelModel()

        #
        # Дополнительные окна
        #

        self.history_window = HistoryWindow()

        #
        # Окно
        #

        self.setWindowTitle(
            "ByTop Production Suite"
        )

        self.resize(
            1600,
            900,
        )

        self.init_ui()

    # ---------------------------------------------------------

    def init_ui(self):

        self.toolbar = MainToolBar()

        self.setMenuWidget(
            self.toolbar
        )

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QHBoxLayout(
            central
        )

        splitter = QSplitter(
            Qt.Horizontal
        )

        self.clipboard_panel = ClipboardPanel()

        self.components_table = ComponentsTable()

        self.preview_panel = PreviewPanel()

        splitter.addWidget(
            self.clipboard_panel
        )

        splitter.addWidget(
            self.components_table
        )

        splitter.addWidget(
            self.preview_panel
        )

        splitter.setStretchFactor(
            0,
            2,
        )

        splitter.setStretchFactor(
            1,
            3,
        )

        splitter.setStretchFactor(
            2,
            4,
        )

        splitter.setSizes(
            [
                420,
                520,
                660,
            ]
        )

        layout.addWidget(
            splitter
        )

        #
        # Сигналы панели
        #

        self.toolbar.paste_requested.connect(
            self.paste_from_clipboard
        )

        self.toolbar.new_build_requested.connect(
            self.create_new_build
        )

        self.toolbar.export_pdf_requested.connect(
            self.export_pdf
        )

        self.toolbar.print_requested.connect(
            self.print_label
        )

        self.toolbar.history_requested.connect(
            self.show_history
        )

        self.toolbar.settings_requested.connect(
            self.show_settings
        )

    # ---------------------------------------------------------

    def paste_from_clipboard(self):

        clipboard = QApplication.clipboard()

        text = clipboard.text()

        self.clipboard_panel.set_clipboard_text(
            text
        )

        self.current_configuration = (
            self.parser.parse(text)
        )
        self.current_label.manufacturer = (
            self.preview_panel.manufacturer()
        )

        self.current_label.page_layout = (
            self.preview_panel.layout_mode()
        )
        self.components_table.set_data(
            self.current_configuration
        )

        self.current_label = (
            self.build_service.preview(
                self.current_configuration
            )
        )

        self.preview_panel.set_label(
            self.current_label
        )

    # ---------------------------------------------------------

    def create_new_build(self):

        if not self.current_configuration.items:

            QMessageBox.warning(
                self,
                "Нет данных",
                "Сначала вставьте конфигурацию из буфера."
            )

            return

        self.current_label = (
            self.build_service.create(
                self.current_configuration
            )
        )
        self.current_label.manufacturer = (
            self.preview_panel.manufacturer()
        )

        self.current_label.page_layout = (
            self.preview_panel.layout_mode()
        )
        self.preview_panel.set_label(
            self.current_label
        )

        #
        # Обновляем журнал
        #

        self.history_window.panel.refresh()

        QMessageBox.information(
            self,
            "Готово",
            f"Создано изделие № {self.current_label.serial}"
        )
    # ---------------------------------------------------------

    def export_pdf(self):

        if not self.current_label.title:

            QMessageBox.warning(
                self,
                "Нет данных",
                "Сначала загрузите конфигурацию."
            )
            return

        if not self.current_label.serial:

            QMessageBox.warning(
                self,
                "Нет изделия",
                "Сначала нажмите «Новая сборка»."
            )
            return

        cpu = (
            self.current_label.cpu
            .replace("/", "-")
            .replace(" ", "_")
        )

        filename = (
            f"ByTop_PE_{cpu}_"
            f"SN{self.current_label.serial}.pdf"
        )

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт PDF",
            str(Path.home() / filename),
            "PDF (*.pdf)"
        )

        if not path:
            return

        self.print_engine.export_pdf(
            self.current_label,
            path,
        )

        QMessageBox.information(
            self,
            "Готово",
            "PDF успешно сохранён."
        )

    # ---------------------------------------------------------

    def print_label(self):

        if not self.current_label.title:

            QMessageBox.warning(
                self,
                "Нет данных",
                "Сначала загрузите конфигурацию."
            )
            return

        if not self.current_label.serial:

            QMessageBox.warning(
                self,
                "Нет изделия",
                "Сначала нажмите «Новая сборка»."
            )
            return

        self.print_engine.print_to_printer(
            self.current_label
        )

        QMessageBox.information(
            self,
            "Печать",
            "Документ отправлен на принтер."
        )

    # ---------------------------------------------------------

    def show_history(self):

        self.history_window.panel.refresh()

        self.history_window.show()

        self.history_window.raise_()

        self.history_window.activateWindow()

    # ---------------------------------------------------------

    def show_settings(self):

        dialog = SettingsDialog(self)

        if dialog.exec():

            #
            # Перечитываем настройки
            #

            self.print_engine = PrintEngine()

            QMessageBox.information(
                self,
                "Настройки",
                "Настройки успешно сохранены."
            )
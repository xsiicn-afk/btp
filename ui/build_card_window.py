from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from models.label_model import LabelModel
from printing.print_engine import PrintEngine
from ui.build_card import BuildCard


class BuildCardWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Карточка изделия")
        self.resize(700, 800)

        self.card = BuildCard()
        self.setCentralWidget(self.card)

        self.print_engine = PrintEngine()

        self.label = None

        #
        # Сигналы
        #

        self.card.pdf_requested.connect(
            self.export_pdf
        )

        self.card.print_requested.connect(
            self.print_label
        )

    # ---------------------------------------------------------

    def set_label(
        self,
        label: LabelModel,
    ):

        self.label = label

        self.card.set_label(label)

    # ---------------------------------------------------------

    def export_pdf(self):

        if self.label is None:
            return

        filename = (
            f"SN{self.label.serial}.pdf"
        )

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт PDF",
            str(Path.home() / filename),
            "PDF (*.pdf)",
        )

        if not path:
            return

        self.print_engine.export_pdf(
            self.label,
            path,
        )

        QMessageBox.information(
            self,
            "Готово",
            "PDF успешно создан."
        )

    # ---------------------------------------------------------

    def print_label(self):

        if self.label is None:
            return

        self.print_engine.print_to_printer(
            self.label
        )

        QMessageBox.information(
            self,
            "Печать",
            "Документ отправлен на принтер."
        )
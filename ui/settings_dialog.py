from pathlib import Path

from PySide6.QtPrintSupport import QPrinterInfo
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from services.settings_service import SettingsService


class SettingsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.settings = SettingsService()

        self.setWindowTitle("Настройки")

        self.resize(650, 240)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        # -------------------------------------------------
        # Шаблон Excel
        # -------------------------------------------------

        self.template = QLineEdit(
            self.settings.get("template_path")
        )

        btn_template = QPushButton("...")

        btn_template.clicked.connect(
            self.select_template
        )

        row = QHBoxLayout()

        row.addWidget(self.template)
        row.addWidget(btn_template)

        form.addRow(
            QLabel("Шаблон Excel"),
            row,
        )

        # -------------------------------------------------
        # Папка PDF
        # -------------------------------------------------

        self.pdf = QLineEdit(
            self.settings.get("pdf_folder")
        )

        btn_pdf = QPushButton("...")

        btn_pdf.clicked.connect(
            self.select_pdf
        )

        row = QHBoxLayout()

        row.addWidget(self.pdf)
        row.addWidget(btn_pdf)

        form.addRow(
            QLabel("Папка PDF"),
            row,
        )

        # -------------------------------------------------
        # Принтер
        # -------------------------------------------------

        self.printer = QComboBox()

        current = self.settings.get("printer")

        for printer in QPrinterInfo.availablePrinters():

            self.printer.addItem(printer.printerName())

        index = self.printer.findText(current)

        if index >= 0:
            self.printer.setCurrentIndex(index)

        form.addRow(
            QLabel("Принтер"),
            self.printer,
        )

        layout.addLayout(form)

        # -------------------------------------------------
        # Кнопки
        # -------------------------------------------------

        buttons = QHBoxLayout()

        ok = QPushButton("Сохранить")
        cancel = QPushButton("Отмена")

        ok.clicked.connect(self.save)
        cancel.clicked.connect(self.reject)

        buttons.addStretch()

        buttons.addWidget(ok)
        buttons.addWidget(cancel)

        layout.addLayout(buttons)

    # ---------------------------------------------------------

    def select_template(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Шаблон Excel",
            self.template.text(),
            "Excel (*.xlsx *.xlsm)",
        )

        if file:
            self.template.setText(file)

    # ---------------------------------------------------------

    def select_pdf(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Папка PDF",
            self.pdf.text() or str(Path.home()),
        )

        if folder:
            self.pdf.setText(folder)

    # ---------------------------------------------------------

    def save(self):

        self.settings.set(
            "template_path",
            self.template.text(),
        )

        self.settings.set(
            "pdf_folder",
            self.pdf.text(),
        )

        self.settings.set(
            "printer",
            self.printer.currentText(),
        )

        self.accept()
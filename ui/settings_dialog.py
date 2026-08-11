from PySide6.QtPrintSupport import QPrinterInfo
from PySide6.QtWidgets import (
QComboBox,
QDialog,
QFormLayout,
QHBoxLayout,
QLabel,
QPushButton,
QVBoxLayout,
)

from services.settings_service import SettingsService

class SettingsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.settings = SettingsService()

        self.setWindowTitle("Настройки")

        self.resize(520, 180)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        # -------------------------------------------------
        # Принтер спецификации
        # -------------------------------------------------

        self.spec_printer = QComboBox()

        # -------------------------------------------------
        # Принтер паспорта
        # -------------------------------------------------

        self.passport_printer = QComboBox()

        # -------------------------------------------------
        # Принтер стикера
        # -------------------------------------------------

        self.sticker_printer = QComboBox()

        printers = [
            printer.printerName()
            for printer
            in QPrinterInfo.availablePrinters()
        ]

        self.spec_printer.addItems(printers)
        self.passport_printer.addItems(printers)
        self.sticker_printer.addItems(printers)

        self._select_current(
            self.spec_printer,
            self.settings.get_spec_printer(),
        )

        self._select_current(
            self.passport_printer,
            self.settings.get_passport_printer(),
        )

        self._select_current(
            self.sticker_printer,
            self.settings.get_sticker_printer(),
        )

        form.addRow(
            QLabel("Принтер спецификации"),
            self.spec_printer,
        )

        form.addRow(
            QLabel("Принтер паспорта"),
            self.passport_printer,
        )

        form.addRow(
            QLabel("Принтер стикера"),
            self.sticker_printer,
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

    @staticmethod
    def _select_current(
        combo: QComboBox,
        value: str,
    ):

        if not value:
            return

        index = combo.findText(value)

        if index >= 0:
            combo.setCurrentIndex(index)

    # ---------------------------------------------------------

    def save(self):

        self.settings.set_spec_printer(
            self.spec_printer.currentText(),
        )

        self.settings.set_passport_printer(
            self.passport_printer.currentText(),
        )

        self.settings.set_sticker_printer(
            self.sticker_printer.currentText(),
        )

        self.accept()

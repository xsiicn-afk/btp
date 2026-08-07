from PySide6.QtPrintSupport import QPrinterInfo
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
)

from services.settings_service import SettingsService


class SettingsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.settings = SettingsService()

        self.setWindowTitle("Настройки")

        self.resize(700, 260)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        # -------------------------------------------------
        # Шаблон спецификации
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
            QLabel("Шаблон спецификации"),
            row,
        )

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

        ok.clicked.connect(
            self.save
        )

        cancel.clicked.connect(
            self.reject
        )

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

        index = combo.findText(
            value
        )

        if index >= 0:

            combo.setCurrentIndex(
                index
            )

    # ---------------------------------------------------------

    def select_template(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Шаблон спецификации",
            self.template.text(),
            "Excel (*.xlsx *.xlsm)",
        )

        if file:

            self.template.setText(
                file
            )
    # ---------------------------------------------------------

    def save(self):

        self.settings.set(
            "template_path",
            self.template.text(),
        )

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
        
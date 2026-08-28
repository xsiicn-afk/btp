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
from services.template_service import TemplateService


class SettingsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.settings = SettingsService()
        self.templates = TemplateService()

        self.setWindowTitle("Настройки")

        self.resize(520, 240)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        # =================================================
        # Принтеры
        # =================================================

        self.spec_printer = QComboBox()
        self.passport_printer = QComboBox()
        self.sticker_printer = QComboBox()

        printers = [
            printer.printerName()
            for printer in QPrinterInfo.availablePrinters()
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

        # =================================================
        # Профили шаблонов
        # =================================================

        self.template_profile = QComboBox()

        # Храним соответствие:
        # отображаемое имя -> имя папки.
        self.profile_map = {}

        current_folder = (
            self.settings.get_template_profile()
        )

        current_index = 0

        for index, folder in enumerate(
            self.templates.profiles()
        ):

            info = self.templates.profile_info(folder)

            display = info["name"]

            self.profile_map[display] = folder

            self.template_profile.addItem(display)

            if folder == current_folder:
                current_index = index

        self.template_profile.setCurrentIndex(current_index)

        form.addRow(
            QLabel("Профиль шаблонов"),
            self.template_profile,
        )

        layout.addLayout(form)

        # =================================================
        # Кнопки
        # =================================================

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

        display = self.template_profile.currentText()

        folder = self.profile_map.get(
            display,
            display,
        )

        self.settings.set_template_profile(
            folder,
        )

        self.accept()
from pathlib import Path

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QInputDialog,
    QPlainTextEdit,
    QSpinBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
    QInputDialog,
)

from parser.basic_parser import BasicParser

from models.configuration import Configuration
from models.label_model import LabelModel

from printing.print_engine import PrintEngine

from services.build_service import BuildService

from ui.clipboard_panel import ClipboardPanel
from ui.components_table import ComponentsTable
from ui.toolbar import MainToolBar
from ui.settings_dialog import SettingsDialog
from ui.history_window import HistoryWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # -------------------------------------------------
        # Сервисы
        # -------------------------------------------------

        self.parser = BasicParser()

        self.build_service = BuildService()

        self.print_engine = PrintEngine()

        # -------------------------------------------------
        # Данные
        # -------------------------------------------------

        self.current_configuration = (
            Configuration()
        )

        self.current_label = (
            LabelModel()
        )

        # -------------------------------------------------
        # Дополнительные окна
        # -------------------------------------------------

        self.history_window = (
            HistoryWindow()
        )

        # -------------------------------------------------
        # Главное окно
        # -------------------------------------------------

        self.setWindowTitle(
            "ByTop Production Suite"
        )

        self.resize(
            1700,
            950,
        )

        self.init_ui()

    # ---------------------------------------------------------

    def init_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        root_layout = QHBoxLayout(
            central
        )

        splitter = QSplitter(
            Qt.Horizontal
        )

        # =================================================
        # Левая панель
        # =================================================

        left = QWidget()

        left_layout = QVBoxLayout(
            left
        )

        left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        left_layout.setSpacing(
            8
        )

        # -------------------------------------------------
        # Кнопки
        #
        # Теперь toolbar является частью левой панели,
        # а не отдельной строкой над всем окном.
        # -------------------------------------------------

        self.toolbar = MainToolBar()

        left_layout.addWidget(
            self.toolbar
        )

        # -------------------------------------------------
        # Исходный текст из 1С
        # -------------------------------------------------

        self.clipboard_panel = (
            ClipboardPanel()
        )

        left_layout.addWidget(
            self.clipboard_panel,
            1,
        )

        splitter.addWidget(
            left
        )

        # =================================================
        # Правая панель
        # =================================================

        right = QWidget()

        right_layout = QVBoxLayout(
            right
        )

        right_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # -------------------------------------------------
        # Комплектующие
        # -------------------------------------------------

        self.components_table = (
            ComponentsTable()
        )

        right_layout.addWidget(
            self.components_table,
            1,
        )

        # -------------------------------------------------
        # Название модели
        # -------------------------------------------------

        self.model_name_title = QLabel(
            "Наименование модели:"
        )

        self.model_name_title.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
                font-size: 14px;
                margin-top: 8px;
            }
            """
        )

        right_layout.addWidget(
            self.model_name_title
        )

        self.model_name_preview = (
            QPlainTextEdit()
        )

        # Название можно исправлять вручную.

        self.model_name_preview.setReadOnly(
            False
        )

        self.model_name_preview.setPlaceholderText(
            (
                "После разбора конфигурации здесь "
                "появится сформированное наименование. "
                "При необходимости его можно исправить."
            )
        )

        self.model_name_preview.setMaximumHeight(
            90
        )

        right_layout.addWidget(
            self.model_name_preview
        )

        # =================================================
        # Гарантия
        # =================================================

        warranty_layout = QHBoxLayout()

        warranty_layout.setContentsMargins(
            0,
            4,
            0,
            0,
        )

        warranty_layout.setSpacing(
            8
        )

        self.warranty_label = QLabel(
            "Гарантия, мес.:"
        )

        self.warranty_label.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
                font-size: 14px;
            }
            """
        )

        self.warranty_spin = QSpinBox()

        # -------------------------------------------------
        # Допускаем срок от 0 до 120 месяцев.
        #
        # 0 можно использовать для изделия
        # без гарантийного срока.
        # -------------------------------------------------

        self.warranty_spin.setRange(
            0,
            120,
        )

        self.warranty_spin.setValue(
            36
        )

        self.warranty_spin.setSuffix(
            " мес."
        )

        self.warranty_spin.setFixedWidth(
            110
        )

        warranty_layout.addWidget(
            self.warranty_label
        )

        warranty_layout.addWidget(
            self.warranty_spin
        )

        warranty_layout.addStretch()

        right_layout.addLayout(
            warranty_layout
        )

        # =================================================
        # Добавляем правую панель
        # =================================================

        splitter.addWidget(
            right
        )

        # -------------------------------------------------
        # Размеры панелей
        # -------------------------------------------------

        splitter.setStretchFactor(
            0,
            2,
        )

        splitter.setStretchFactor(
            1,
            5,
        )

        splitter.setSizes(
            [
                430,
                1270,
            ]
        )

        root_layout.addWidget(
            splitter
        )

        # =================================================
        # Сигналы
        # =================================================

        self.toolbar.paste_requested.connect(
            self.refresh_configuration
        )

        self.toolbar.new_build_requested.connect(
            self.create_new_build
        )

        self.toolbar.history_requested.connect(
            self.show_history
        )

        self.toolbar.settings_requested.connect(
            self.show_settings
        )

    # ---------------------------------------------------------

    def refresh_configuration(self):
        """
        Повторно разбирает исходный текст.

        Перед повторным парсингом сохраняет
        введённые пользователем:

        - количества;
        - серийные номера комплектующих.

        Гарантия при обновлении не меняется.
        """

        text = (
            self.clipboard_panel
            .toPlainText()
        )

        if not text.strip():

            QMessageBox.warning(
                self,
                "Нет данных",
                (
                    "Левое поле пустое.\n\n"
                    "Вставьте спецификацию из 1С."
                ),
            )

            return

        # -------------------------------------------------
        # Сохраняем данные таблицы
        # -------------------------------------------------

        quantities = (
            self.components_table
            .get_quantities()
        )

        serial_numbers = (
            self.components_table
            .get_serial_numbers()
        )

        # -------------------------------------------------
        # Новый разбор текста
        # -------------------------------------------------

        configuration = (
            self.parser.parse(
                text
            )
        )

        # -------------------------------------------------
        # Возвращаем ручные значения
        # -------------------------------------------------

        for item in configuration.items:

            key = (
                item.category.value,
                item.name.strip(),
            )

            if key in quantities:

                item.quantity = (
                    quantities[key]
                )

            if key in serial_numbers:

                item.serial_number = (
                    serial_numbers[key]
                )

        self.current_configuration = (
            configuration
        )

        # -------------------------------------------------
        # Предпросмотр
        # -------------------------------------------------

        self.current_label = (
            self.build_service.preview(
                self.current_configuration
            )
        )

        # -------------------------------------------------
        # Таблица
        # -------------------------------------------------

        self.components_table.set_data(
            self.current_configuration
        )

        # -------------------------------------------------
        # Автоматически сформированное название
        # -------------------------------------------------

        self.model_name_preview.setPlainText(
            self.current_label.model_name
            or ""
        )

    # ---------------------------------------------------------

    def create_new_build(self):
        """
        Создаёт одно или несколько изделий подряд.

        Перед созданием запрашивает количество изделий.
        """

        if not self.current_configuration.items:

            QMessageBox.warning(
                self,
                "Нет данных",
                (
                    "Сначала вставьте конфигурацию "
                    "и нажмите «Обновить»."
                ),
            )

            return

        # -------------------------------------------------
        # Запрашиваем количество изделий
        # -------------------------------------------------

        quantity, ok = QInputDialog.getInt(
            self,
            "Создание изделий",
            "Количество изделий:",
            1,
            1,
            100,
            1,
        )

        if not ok:
            return

        # -------------------------------------------------
        # Переносим актуальные данные из таблицы
        # -------------------------------------------------

        self.components_table.apply_to_configuration(
            self.current_configuration
        )

        manual_model_name = (
            self.model_name_preview
            .toPlainText()
            .strip()
        )

        warranty_months = self.warranty_spin.value()

        created_serials = []

        # -------------------------------------------------
        # Создаём серию изделий
        # -------------------------------------------------

        for _ in range(quantity):

            label = self.build_service.create(
                self.current_configuration,
                manual_model_name,
                warranty_months,
            )

            created_serials.append(label.serial)

            self.current_label = label

        # -------------------------------------------------
        # Обновляем историю
        # -------------------------------------------------

        self.history_window.panel.refresh()

        # -------------------------------------------------
        # Оставляем последнее имя в редакторе
        # -------------------------------------------------

        self.model_name_preview.setPlainText(
            self.current_label.model_name
            or ""
        )

        # -------------------------------------------------
        # Очищаем только серийники комплектующих
        # -------------------------------------------------

        for item in self.current_configuration.items:
            item.serial_number = ""

        self.components_table.clear_serial_numbers()

        # -------------------------------------------------
        # Сообщение
        # -------------------------------------------------

        if quantity == 1:

            text = (
                "Создано изделие № "
                f"{created_serials[0]}\\n\\n"
                "Гарантия: "
                f"{warranty_months} мес.\\n\\n"
                "Серийные номера комплектующих "
                "очищены для следующей сборки."
            )

        else:

            text = (
                f"Создано изделий: {quantity}\\n\\n"
                f"Первый номер: {created_serials[0]}\\n"
                f"Последний номер: {created_serials[-1]}\\n\\n"
                "Гарантия: "
                f"{warranty_months} мес.\\n\\n"
                "Серийные номера комплектующих "
                "очищены для следующей сборки."
            )

        QMessageBox.information(
            self,
            "Готово",
            text,
        )

        # -------------------------------------------------
        # Сразу готовимся к следующему сканированию
        # -------------------------------------------------

        self.components_table.focus_first_serial()

    # ---------------------------------------------------------

    def show_history(self):

        self.history_window.panel.refresh()

        self.history_window.show()

        self.history_window.raise_()

        self.history_window.activateWindow()

    # ---------------------------------------------------------

    def show_settings(self):

        dialog = SettingsDialog(
            self
        )

        dialog.exec()

    # ---------------------------------------------------------

    def export_excel(self):

        QMessageBox.information(
            self,
            "В разработке",
            (
                "Экспорт будет работать "
                "через шаблон Excel."
            ),
        )

    # ---------------------------------------------------------

    def print_label(self):

        QMessageBox.information(
            self,
            "Информация",
            (
                "Печать будет доступна "
                "из карточки изделия."
            ),
        )

    # ---------------------------------------------------------

    def open_configuration(self):

        filename, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Открыть конфигурацию",
                str(
                    Path.home()
                ),
                (
                    "Текстовые файлы (*.txt);;"
                    "Все файлы (*.*)"
                ),
            )
        )

        if not filename:

            return

        try:

            with open(
                filename,
                "r",
                encoding="utf-8",
            ) as file:

                text = file.read()

            self.clipboard_panel.set_clipboard_text(
                text
            )

            self.refresh_configuration()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка",
                (
                    "Не удалось открыть файл.\n\n"
                    f"{error}"
                ),
            )

    # ---------------------------------------------------------

    def closeEvent(
        self,
        event,
    ):

        if self.history_window.isVisible():

            self.history_window.close()

        event.accept()
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from models.label_model import LabelModel

from printing.print_engine import PrintEngine

from services.build_history_service import (
    BuildHistoryService,
)

from ui.build_card import BuildCard


class BuildCardWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Карточка изделия"
        )

        self.resize(
            850,
            900,
        )

        #
        # Модель
        #

        self.label: LabelModel | None = None

        #
        # Сервисы
        #

        self.history = BuildHistoryService()

        self.print_engine = PrintEngine()

        #
        # Интерфейс
        #

        self.card = BuildCard()

        self.setCentralWidget(
            self.card
        )

        #
        # Сигналы
        #

        self.card.save_requested.connect(
            self.save
        )

        self.card.specification_requested.connect(
            self.print_specification
        )

        self.card.passport_requested.connect(
            self.print_passport
        )

        self.card.sticker_requested.connect(
            self.print_sticker
        )

    # ---------------------------------------------------------

    def set_label(
        self,
        label: LabelModel,
    ):

        self.label = label

        self.card.set_label(
            label
        )

        self.card.set_print_enabled(
            True
        )

        self.update_title()

    # ---------------------------------------------------------

    def update_title(
        self,
    ):

        if self.label is None:

            self.setWindowTitle(
                "Карточка изделия"
            )

            return

        title = self.label.title

        if not title:

            title = self.label.internal_name

        self.setWindowTitle(
            f"{self.label.serial} — {title}"
        )

    # ---------------------------------------------------------

    def clear(
        self,
    ):

        self.label = None

        self.card.clear()

        self.update_title()
    # ---------------------------------------------------------

    def save(
        self,
    ):

        if self.label is None:

            return

        try:

            #
            # Пока сохраняем только новые изделия.
            # Полноценное редактирование с увеличением
            # версии добавим следующим этапом.
            #

            exists = self.history.load_label(
                self.label.serial
            )

            if exists is None:

                self.history.save(
                    self.label
                )

            QMessageBox.information(
                self,
                "Сохранено",
                "Изделие успешно сохранено."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(error)
            )

    # ---------------------------------------------------------

    def print_specification(
        self,
    ):

        if self.label is None:

            return

        self.print_engine.print_to_printer(
            self.label
        )

        self.history.print_specification(
            self.label.serial
        )

        self.card.set_specification_printed(
            True
        )

        QMessageBox.information(
            self,
            "Печать",
            "Спецификация отправлена на печать."
        )

    # ---------------------------------------------------------

    def print_passport(
        self,
    ):

        if self.label is None:

            return

        #
        # Пока используется тот же PrintEngine.
        #

        self.print_engine.print_to_printer(
            self.label
        )

        self.history.print_passport(
            self.label.serial
        )

        self.card.set_passport_printed(
            True
        )

        QMessageBox.information(
            self,
            "Печать",
            "Паспорт отправлен на печать."
        )

    # ---------------------------------------------------------

    def print_sticker(
        self,
    ):

        if self.label is None:

            return

        #
        # Пока используется тот же PrintEngine.
        #

        self.print_engine.print_to_printer(
            self.label
        )

        self.history.print_sticker(
            self.label.serial
        )

        self.card.set_sticker_printed(
            True
        )

        QMessageBox.information(
            self,
            "Печать",
            "Стикер отправлен на печать."
        )
    # ---------------------------------------------------------

    def current_label(
        self,
    ) -> LabelModel | None:

        return self.label

    # ---------------------------------------------------------

    def has_label(
        self,
    ) -> bool:

        return self.label is not None

    # ---------------------------------------------------------

    def refresh(
        self,
    ):

        if self.label is None:

            return

        self.card.set_label(
            self.label
        )

        self.update_title()

    # ---------------------------------------------------------

    def show_message(
        self,
        title: str,
        text: str,
    ):

        QMessageBox.information(
            self,
            title,
            text,
        )

    # ---------------------------------------------------------

    def show_error(
        self,
        title: str,
        text: str,
    ):

        QMessageBox.critical(
            self,
            title,
            text,
        )

    # ---------------------------------------------------------

    def closeEvent(
        self,
        event,
    ):

        self.label = None

        super().closeEvent(
            event
        )

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from services.build_history_service import BuildHistoryService

from ui.build_card_window import BuildCardWindow
from ui.history_panel import HistoryPanel


class HistoryWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Производство"
        )

        self.resize(
            1200,
            750,
        )

        #
        # Сервисы
        #

        self.history = BuildHistoryService()

        #
        # Интерфейс
        #

        self.panel = HistoryPanel()

        self.setCentralWidget(
            self.panel
        )

        self.viewer = BuildCardWindow()

        #
        # Сигналы
        #

        self.panel.build_selected.connect(
            self.open_build
        )

        self.panel.specification_requested.connect(
            self.print_specifications
        )

        self.panel.passport_requested.connect(
            self.print_passports
        )

        self.panel.sticker_requested.connect(
            self.print_stickers
        )
    # ---------------------------------------------------------

    def refresh(self):

        self.panel.refresh()

    # ---------------------------------------------------------

    def open_build(
        self,
        serial: str,
    ):

        label = self.history.load_label(
            serial
        )

        if label is None:

            QMessageBox.warning(
                self,
                "Ошибка",
                "Изделие не найдено.",
            )

            return

        self.viewer.set_label(
            label
        )

        self.viewer.show()

        self.viewer.raise_()

        self.viewer.activateWindow()

    # ---------------------------------------------------------

    def print_specifications(
        self,
        serials: list[str],
    ):

        printed = 0

        for serial in serials:

            if self.history.print_specification(
                serial
            ):

                printed += 1

        self.panel.mark_specification_printed(
            serials
        )

        QMessageBox.information(
            self,
            "Печать",
            f"Распечатано спецификаций: {printed}",
        )
    # ---------------------------------------------------------

    def print_passports(
        self,
        serials: list[str],
    ):

        printed = 0

        for serial in serials:

            if self.history.print_passport(
                serial
            ):

                printed += 1

        self.panel.mark_passport_printed(
            serials
        )

        QMessageBox.information(
            self,
            "Печать",
            f"Распечатано паспортов: {printed}",
        )

    # ---------------------------------------------------------

    def print_stickers(
        self,
        serials: list[str],
    ):

        printed = 0

        for serial in serials:

            if self.history.print_sticker(
                serial
            ):

                printed += 1

        self.panel.mark_sticker_printed(
            serials
        )

        QMessageBox.information(
            self,
            "Печать",
            f"Распечатано наклеек: {printed}",
        )
    # ---------------------------------------------------------

    def update(self):

        """
        Обновить список изделий.
        """

        self.refresh()

    # ---------------------------------------------------------

    def showEvent(
        self,
        event,
    ):

        super().showEvent(
            event
        )

        self.refresh()

    # ---------------------------------------------------------

    def closeEvent(
        self,
        event,
    ):

        if self.viewer.isVisible():

            self.viewer.close()

        super().closeEvent(
            event
        )

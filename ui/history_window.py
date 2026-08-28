from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QMessageBox,
)

from services.build_history_service import BuildHistoryService

from ui.build_card_window import BuildCardWindow
from ui.history_panel import HistoryPanel
from ui.specification_print_dialog import (
    SpecificationPrintDialog,
)


class HistoryWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Производство")

        self.resize(1200, 750)

        self.history = BuildHistoryService()

        self.panel = HistoryPanel()

        self.setCentralWidget(self.panel)

        self.viewer = BuildCardWindow()

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

        label = self.history.load_label(serial)

        if label is None:

            QMessageBox.warning(
                self,
                "Ошибка",
                "Изделие не найдено.",
            )

            return

        self.viewer.set_label(label)

        self.viewer.show()
        self.viewer.raise_()
        self.viewer.activateWindow()

    # ---------------------------------------------------------

    def print_specifications(
        self,
        serials: list[str],
    ):

        if not serials:
            return

        dialog = SpecificationPrintDialog(
            len(serials),
            self,
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        printed = 0

        try:

            for serial in serials:

                if self.history.print_specification(serial):
                    printed += 1

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка печати",
                (
                    "Не удалось распечатать "
                    "спецификацию.\n\n"
                    f"{error}"
                ),
            )

            return

        if printed:

            self.panel.mark_specification_printed(
                serials
            )

        QMessageBox.information(
            self,
            "Печать",
            (
                "Распечатано спецификаций: "
                f"{printed}"
            ),
        )

    # ---------------------------------------------------------

    def print_passports(
        self,
        serials: list[str],
    ):

        if not serials:
            return

        printed = 0

        try:

            for serial in serials:

                if self.history.print_passport(serial):
                    printed += 1

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка печати",
                (
                    "Не удалось распечатать "
                    "паспорт.\n\n"
                    f"{error}"
                ),
            )

            return

        if printed:

            self.panel.mark_passport_printed(
                serials
            )

        QMessageBox.information(
            self,
            "Печать",
            (
                "Распечатано паспортов: "
                f"{printed}"
            ),
        )

    # ---------------------------------------------------------

    def print_stickers(
        self,
        serials: list[str],
    ):

        if not serials:
            return

        printed_serials = []

        try:

            for serial in serials:

                if self.history.print_sticker(serial):
                    printed_serials.append(serial)

        except Exception as error:

            if printed_serials:

                self.panel.mark_sticker_printed(
                    printed_serials
                )

            QMessageBox.critical(
                self,
                "Ошибка печати наклейки",
                (
                    "Не удалось распечатать "
                    "наклейку.\n\n"
                    f"{error}"
                ),
            )

            return

        if printed_serials:

            self.panel.mark_sticker_printed(
                printed_serials
            )

        QMessageBox.information(
            self,
            "Печать",
            (
                "Распечатано наклеек: "
                f"{len(printed_serials)}"
            ),
        )

    # ---------------------------------------------------------

    def update(self):

        self.refresh()

    # ---------------------------------------------------------

    def showEvent(
        self,
        event,
    ):

        super().showEvent(event)

        self.refresh()

    # ---------------------------------------------------------

    def closeEvent(
        self,
        event,
    ):

        if self.viewer.isVisible():
            self.viewer.close()

        try:
            self.history.close()
        except Exception:
            pass

        super().closeEvent(event)
from PySide6.QtWidgets import QMainWindow, QMessageBox

from services.build_history_service import BuildHistoryService

from ui.build_card_window import BuildCardWindow
from ui.history_panel import HistoryPanel


class HistoryWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "История производства"
        )

        self.resize(
            1000,
            700,
        )

        self.history = BuildHistoryService()

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
                "Изделие не найдено."
            )

            return

        self.viewer.set_label(
            label
        )

        self.viewer.show()

        self.viewer.raise_()

        self.viewer.activateWindow()
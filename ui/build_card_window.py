from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from models.label_model import LabelModel

from services.build_history_service import (
    BuildHistoryService,
)

from ui.build_card import BuildCard


class BuildCardWindow(QMainWindow):
    """
    Окно просмотра карточки изделия.

    Изменять можно только серийные номера
    комплектующих двойным щелчком по S/N.
    """

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Карточка изделия"
        )

        self.resize(
            1000,
            750,
        )

        self.label: LabelModel | None = None

        # =================================================
        # Сервис истории
        # =================================================

        self.history_service = (
            BuildHistoryService()
        )

        # =================================================
        # Карточка
        # =================================================

        self.card = BuildCard()

        self.setCentralWidget(
            self.card
        )

        # -------------------------------------------------
        # Сохранение изменённого S/N
        # -------------------------------------------------

        self.card.serial_number_changed.connect(
            self.update_serial_number
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

        self.update_title()

    # ---------------------------------------------------------

    def update_serial_number(
        self,
        item_id: int,
        serial_number: str,
    ):
        """
        Сохраняет изменённый серийный номер
        комплектующего непосредственно в БД.
        """

        try:

            success = (
                self.history_service
                .update_item_serial(
                    item_id,
                    serial_number,
                )
            )

            if not success:

                QMessageBox.warning(
                    self,
                    "Серийный номер",
                    (
                        "Не удалось найти "
                        "комплектующее в базе."
                    ),
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка",
                (
                    "Не удалось сохранить "
                    "серийный номер.\n\n"
                    f"{error}"
                ),
            )

    # ---------------------------------------------------------

    def update_title(
        self,
    ):

        if self.label is None:

            self.setWindowTitle(
                "Карточка изделия"
            )

            return

        serial = (
            self.label.serial
            or ""
        )

        model_name = (
            self.label.model_name
            or "Системный блок"
        )

        if serial:

            self.setWindowTitle(
                f"{serial} — {model_name}"
            )

        else:

            self.setWindowTitle(
                model_name
            )

    # ---------------------------------------------------------

    def clear(
        self,
    ):

        self.label = None

        self.card.clear()

        self.update_title()

    # ---------------------------------------------------------

    def current_label(
        self,
    ) -> LabelModel | None:

        return self.label

    # ---------------------------------------------------------

    def has_label(
        self,
    ) -> bool:

        return (
            self.label is not None
        )

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

    def closeEvent(
        self,
        event,
    ):

        self.label = None

        super().closeEvent(
            event
        )
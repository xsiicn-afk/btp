from PySide6.QtCore import Signal

from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QToolBar,
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

    Также доступно удаление изделия
    из истории производства.
    """

    # ---------------------------------------------------------
    # Сигнал:
    #
    # Передаём серийный номер удалённого изделия,
    # чтобы окно истории могло обновить список.
    # ---------------------------------------------------------

    build_deleted = Signal(str)

    # ---------------------------------------------------------

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
        # Панель инструментов
        # =================================================

        self.toolbar = QToolBar(
            "Действия",
            self,
        )

        self.toolbar.setMovable(
            False
        )

        self.addToolBar(
            self.toolbar
        )

        # -------------------------------------------------
        # Действие удаления
        # -------------------------------------------------

        self.delete_action = QAction(
            "Удалить изделие",
            self,
        )

        self.delete_action.setToolTip(
            "Удалить изделие из истории производства"
        )

        self.delete_action.triggered.connect(
            self.delete_build
        )

        self.toolbar.addAction(
            self.delete_action
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

        # -------------------------------------------------
        # Пока изделие не выбрано,
        # удаление недоступно.
        # -------------------------------------------------

        self.delete_action.setEnabled(
            False
        )

    # =========================================================
    # Загрузка карточки
    # =========================================================

    def set_label(
        self,
        label: LabelModel,
    ):

        self.label = label

        self.card.set_label(
            label
        )

        self.delete_action.setEnabled(
            bool(
                label.serial
            )
        )

        self.update_title()

    # =========================================================
    # Сохранение S/N комплектующих
    # =========================================================

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

    # =========================================================
    # Удаление изделия
    # =========================================================

    def delete_build(
        self,
    ):
        """
        Удаляет текущее изделие из истории
        после подтверждения пользователя.

        Одновременно удаляются все комплектующие
        и их серийные номера.
        """

        # -------------------------------------------------
        # Проверяем, есть ли открытое изделие.
        # -------------------------------------------------

        if self.label is None:

            return

        serial = (
            self.label.serial
            or ""
        ).strip()

        if not serial:

            QMessageBox.warning(
                self,
                "Удаление",
                "Не удалось определить серийный номер изделия.",
            )

            return

        model_name = (
            self.label.model_name
            or "Системный блок"
        )

        # -------------------------------------------------
        # Подтверждение
        # -------------------------------------------------

        answer = QMessageBox.question(
            self,
            "Удаление изделия",
            (
                "Вы действительно хотите удалить изделие?\n\n"
                f"Серийный номер: {serial}\n"
                f"Наименование: {model_name}\n\n"
                "Будут удалены также все сохранённые "
                "серийные номера его комплектующих.\n\n"
                "Отменить это действие будет невозможно."
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):

            return

        # -------------------------------------------------
        # Перед удалением завершаем возможное
        # редактирование S/N.
        # -------------------------------------------------

        try:

            self.card.commit_pending_edit()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка",
                (
                    "Не удалось завершить "
                    "редактирование серийного номера.\n\n"
                    f"{error}"
                ),
            )

            return

        # -------------------------------------------------
        # Удаляем из БД.
        # -------------------------------------------------

        try:

            success = (
                self.history_service
                .delete_build(
                    serial
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка удаления",
                (
                    "Не удалось удалить изделие.\n\n"
                    f"{error}"
                ),
            )

            return

        if not success:

            QMessageBox.warning(
                self,
                "Удаление",
                (
                    "Изделие не найдено в базе данных."
                ),
            )

            return

        # -------------------------------------------------
        # Запоминаем номер для сигнала.
        # -------------------------------------------------

        deleted_serial = serial

        # -------------------------------------------------
        # Очищаем карточку.
        # -------------------------------------------------

        self.label = None

        self.card.clear()

        self.delete_action.setEnabled(
            False
        )

        self.update_title()

        # -------------------------------------------------
        # Сообщаем окну истории,
        # что изделие удалено.
        # -------------------------------------------------

        self.build_deleted.emit(
            deleted_serial
        )

        # -------------------------------------------------
        # Закрываем карточку.
        # -------------------------------------------------

        QMessageBox.information(
            self,
            "Изделие удалено",
            (
                f"Изделие № {deleted_serial} "
                "успешно удалено из истории."
            ),
        )

        self.close()

    # =========================================================
    # Заголовок
    # =========================================================

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

    # =========================================================
    # Очистка
    # =========================================================

    def clear(
        self,
    ):

        self.label = None

        self.card.clear()

        self.delete_action.setEnabled(
            False
        )

        self.update_title()

    # =========================================================
    # Текущая карточка
    # =========================================================

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

    # =========================================================
    # Обновление
    # =========================================================

    def refresh(
        self,
    ):

        if self.label is None:

            return

        self.card.set_label(
            self.label
        )

        self.delete_action.setEnabled(
            bool(
                self.label.serial
            )
        )

        self.update_title()

    # =========================================================
    # Закрытие
    # =========================================================

    def closeEvent(
        self,
        event,
    ):
        """
        Перед закрытием окна принудительно завершаем
        редактирование активной ячейки.

        Это гарантирует сохранение последнего введённого
        серийного номера даже если оператор сразу закрыл
        окно или нажал печать.
        """

        try:

            self.card.commit_pending_edit()

        except Exception:

            pass

        self.label = None

        super().closeEvent(
            event
        )
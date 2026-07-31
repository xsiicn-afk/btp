from PySide6.QtCore import (
    Qt,
    Signal,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)

from models.label_model import LabelModel


class BuildCard(QWidget):
    """
    Карточка созданного изделия.

    Основной режим — просмотр.

    Серийный номер комплектующего можно
    изменить двойным щелчком по колонке S/N.
    """

    # item_id, новый S/N
    serial_number_changed = Signal(
        int,
        str,
    )

    SERIAL_COLUMN = 3

    def __init__(self):
        super().__init__()

        self.current_label_data = None

        # Не даёт itemChanged срабатывать,
        # пока таблица программно заполняется.
        self._loading = False

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        root.setSpacing(
            10
        )

        # =====================================================
        # Заголовок
        # =====================================================

        self.title = QLabel(
            "Карточка изделия"
        )

        self.title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        root.addWidget(
            self.title
        )

        self.model = QLabel()

        self.model.setWordWrap(
            True
        )

        self.model.setStyleSheet(
            "font-size:15px;font-weight:bold;"
        )

        root.addWidget(
            self.model
        )

        # =====================================================
        # Общая информация
        # =====================================================

        info_frame = QFrame()

        info_frame.setFrameShape(
            QFrame.Box
        )

        info_layout = QGridLayout(
            info_frame
        )

        info_layout.setColumnStretch(
            1,
            1,
        )

        self.serial = QLabel()
        self.article = QLabel()
        self.date = QLabel()
        self.operating_system = QLabel()
        self.warranty = QLabel()
        self.created_by = QLabel()
        self.version = QLabel()

        fields = (
            (
                "Серийный номер",
                self.serial,
            ),
            (
                "Артикул",
                self.article,
            ),
            (
                "Дата производства",
                self.date,
            ),
            (
                "Операционная система",
                self.operating_system,
            ),
            (
                "Гарантия",
                self.warranty,
            ),
            (
                "Создал",
                self.created_by,
            ),
            (
                "Версия",
                self.version,
            ),
        )

        for row, (
            caption,
            widget,
        ) in enumerate(fields):

            caption_widget = QLabel(
                caption
            )

            caption_widget.setStyleSheet(
                "font-weight:bold;"
            )

            info_layout.addWidget(
                caption_widget,
                row,
                0,
            )

            info_layout.addWidget(
                widget,
                row,
                1,
            )

        root.addWidget(
            info_frame
        )

        # =====================================================
        # Полный состав
        # =====================================================

        items_frame = QFrame()

        items_frame.setFrameShape(
            QFrame.Box
        )

        items_layout = QVBoxLayout(
            items_frame
        )

        items_title = QLabel(
            "Комплектующие и серийные номера"
        )

        items_title.setStyleSheet(
            "font-weight:bold;"
        )

        items_layout.addWidget(
            items_title
        )

        self.items_table = QTableWidget()

        self.items_table.setColumnCount(
            4
        )

        self.items_table.setHorizontalHeaderLabels(
            [
                "Категория",
                "Наименование",
                "Кол-во",
                "Серийный номер",
            ]
        )

        # -------------------------------------------------
        # Редактор сам по себе не запускается.
        #
        # Мы запускаем его вручную только после
        # двойного щелчка по S/N.
        # -------------------------------------------------

        self.items_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.items_table.setSelectionBehavior(
            QAbstractItemView.SelectItems
        )

        self.items_table.verticalHeader().setVisible(
            False
        )

        header = (
            self.items_table
            .horizontalHeader()
        )

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents,
        )

        self.items_table.setMinimumHeight(
            260
        )

        # -------------------------------------------------
        # Редактирование S/N
        # -------------------------------------------------

        self.items_table.itemDoubleClicked.connect(
            self._item_double_clicked
        )

        self.items_table.itemChanged.connect(
            self._item_changed
        )

        items_layout.addWidget(
            self.items_table
        )

        root.addWidget(
            items_frame,
            1,
        )

        # =====================================================
        # Статус
        # =====================================================

        status_frame = QFrame()

        status_frame.setFrameShape(
            QFrame.Box
        )

        status_layout = QGridLayout(
            status_frame
        )

        status_title = QLabel(
            "Статус"
        )

        status_title.setStyleSheet(
            "font-weight:bold;"
        )

        status_layout.addWidget(
            status_title,
            0,
            0,
        )

        self.status = QLabel(
            "Создано"
        )

        status_layout.addWidget(
            self.status,
            0,
            1,
        )

        self.specification_status = QLabel()
        self.passport_status = QLabel()
        self.sticker_status = QLabel()

        status_layout.addWidget(
            QLabel("Спецификация"),
            1,
            0,
        )

        status_layout.addWidget(
            self.specification_status,
            1,
            1,
        )

        status_layout.addWidget(
            QLabel("Паспорт"),
            2,
            0,
        )

        status_layout.addWidget(
            self.passport_status,
            2,
            1,
        )

        status_layout.addWidget(
            QLabel("Стикер"),
            3,
            0,
        )

        status_layout.addWidget(
            self.sticker_status,
            3,
            1,
        )

        root.addWidget(
            status_frame
        )

    # ---------------------------------------------------------

    def set_label(
        self,
        label: LabelModel,
    ):

        self.current_label_data = label

        self._loading = True

        try:

            self.model.setText(
                label.model_name
                or "—"
            )

            self.serial.setText(
                label.serial
                or "—"
            )

            self.article.setText(
                str(
                    getattr(
                        label,
                        "article_code",
                        "",
                    )
                    or "—"
                )
            )

            self.date.setText(
                label.date
                or "—"
            )

            self.operating_system.setText(
                label.operating_system
                or "—"
            )

            warranty_months = getattr(
                label,
                "warranty_months",
                36,
            )

            self.warranty.setText(
                f"{warranty_months} мес."
            )

            self.created_by.setText(
                getattr(
                    label,
                    "created_by",
                    "",
                )
                or "—"
            )

            self.version.setText(
                str(
                    getattr(
                        label,
                        "version",
                        1,
                    )
                    or 1
                )
            )

            # =================================================
            # Комплектующие
            # =================================================

            items = getattr(
                label,
                "items",
                [],
            )

            self.items_table.setRowCount(
                len(items)
            )

            for row, item in enumerate(
                items
            ):

                category = getattr(
                    item.category,
                    "value",
                    str(item.category),
                )

                # -----------------------------------------
                # Категория
                # -----------------------------------------

                category_item = (
                    QTableWidgetItem(
                        str(category)
                    )
                )

                category_item.setFlags(
                    category_item.flags()
                    & ~Qt.ItemIsEditable
                )

                self.items_table.setItem(
                    row,
                    0,
                    category_item,
                )

                # -----------------------------------------
                # Наименование
                # -----------------------------------------

                name_item = QTableWidgetItem(
                    item.name
                    or ""
                )

                name_item.setFlags(
                    name_item.flags()
                    & ~Qt.ItemIsEditable
                )

                self.items_table.setItem(
                    row,
                    1,
                    name_item,
                )

                # -----------------------------------------
                # Количество
                # -----------------------------------------

                quantity_item = (
                    QTableWidgetItem(
                        str(
                            item.quantity
                        )
                    )
                )

                quantity_item.setFlags(
                    quantity_item.flags()
                    & ~Qt.ItemIsEditable
                )

                self.items_table.setItem(
                    row,
                    2,
                    quantity_item,
                )

                # -----------------------------------------
                # Серийный номер
                # -----------------------------------------

                serial_item = (
                    QTableWidgetItem(
                        item.serial_number
                        or ""
                    )
                )

                # ID строки build_items храним
                # прямо в ячейке.
                db_id = getattr(
                    item,
                    "db_id",
                    None,
                )

                if db_id is not None:

                    serial_item.setData(
                        Qt.UserRole,
                        int(db_id),
                    )

                self.items_table.setItem(
                    row,
                    self.SERIAL_COLUMN,
                    serial_item,
                )

            self.items_table.resizeRowsToContents()

            # =================================================
            # Статус
            # =================================================

            self.status.setText(
                getattr(
                    label,
                    "status",
                    "Создано",
                )
                or "Создано"
            )

            self.set_specification_printed(
                bool(
                    getattr(
                        label,
                        "spec_printed",
                        False,
                    )
                )
            )

            self.set_passport_printed(
                bool(
                    getattr(
                        label,
                        "passport_printed",
                        False,
                    )
                )
            )

            self.set_sticker_printed(
                bool(
                    getattr(
                        label,
                        "sticker_printed",
                        False,
                    )
                )
            )

        finally:

            self._loading = False

    # ---------------------------------------------------------

    def _item_double_clicked(
        self,
        item: QTableWidgetItem,
    ):
        """
        Разрешаем редактирование исключительно
        ячейки серийного номера.
        """

        if (
            item.column()
            != self.SERIAL_COLUMN
        ):

            return

        if (
            item.data(Qt.UserRole)
            is None
        ):

            return

        self.items_table.editItem(
            item
        )

    # ---------------------------------------------------------

    def _item_changed(
        self,
        item: QTableWidgetItem,
    ):
        """
        После завершения редактирования
        сообщает BuildCardWindow новый S/N.
        """

        if self._loading:

            return

        if (
            item.column()
            != self.SERIAL_COLUMN
        ):

            return

        item_id = item.data(
            Qt.UserRole
        )

        if item_id is None:

            return

        new_serial = (
            item.text()
            or ""
        ).strip()

        # Нормализуем пробелы по краям.

        if item.text() != new_serial:

            self._loading = True

            try:

                item.setText(
                    new_serial
                )

            finally:

                self._loading = False

        # ---------------------------------------------
        # Обновляем LabelModel в памяти.
        # ---------------------------------------------

        if self.current_label_data:

            row = item.row()

            if (
                0 <= row
                < len(
                    self.current_label_data.items
                )
            ):

                self.current_label_data.items[
                    row
                ].serial_number = new_serial

        # ---------------------------------------------
        # Просим окно сохранить изменение.
        # ---------------------------------------------

        self.serial_number_changed.emit(
            int(item_id),
            new_serial,
        )

    # ---------------------------------------------------------

    def set_status(
        self,
        text: str,
    ):

        self.status.setText(
            text
        )

    # ---------------------------------------------------------

    def set_specification_printed(
        self,
        printed: bool,
    ):

        self.specification_status.setText(
            "Напечатана"
            if printed
            else "Не печаталась"
        )

    # ---------------------------------------------------------

    def set_passport_printed(
        self,
        printed: bool,
    ):

        self.passport_status.setText(
            "Напечатан"
            if printed
            else "Не печатался"
        )

    # ---------------------------------------------------------

    def set_sticker_printed(
        self,
        printed: bool,
    ):

        self.sticker_status.setText(
            "Напечатан"
            if printed
            else "Не печатался"
        )

    # ---------------------------------------------------------

    def lock(self):
        pass

    def unlock(self):
        pass

    def set_print_enabled(
        self,
        enabled: bool,
    ):
        pass

    # ---------------------------------------------------------

    def clear(self):

        self.set_label(
            LabelModel()
        )

    # ---------------------------------------------------------

    def current_serial(self) -> str:

        return self.serial.text()

    # ---------------------------------------------------------

    def current_article(self) -> str:

        return self.article.text()

    # ---------------------------------------------------------

    def current_title(self) -> str:

        return self.model.text()

    # ---------------------------------------------------------

    def current_model(self) -> str:

        return self.model.text()

    # ---------------------------------------------------------

    def update_version(
        self,
        version: int,
    ):

        self.version.setText(
            str(version)
        )

    # ---------------------------------------------------------

    def update_creator(
        self,
        creator: str,
    ):

        self.created_by.setText(
            creator
            or "—"
        )

    # ---------------------------------------------------------

    def update_date(
        self,
        date: str,
    ):

        self.date.setText(
            date
            or "—"
        )
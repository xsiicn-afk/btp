from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from models.configuration import Configuration


class ComponentsTable(QTableWidget):
    """
    Таблица распознанных комплектующих.

    Категория и наименование:
        только просмотр.

    Количество:
        редактируется вручную.

    Серийный номер:
        вводится вручную или сканером.

    Enter в столбце серийного номера
    переводит курсор на серийный номер
    следующей строки.
    """

    CATEGORY_COLUMN = 0
    NAME_COLUMN = 1
    QUANTITY_COLUMN = 2
    SERIAL_COLUMN = 3

    def __init__(self):
        super().__init__()

        self.setColumnCount(
            4
        )

        self.setHorizontalHeaderLabels(
            [
                "Категория",
                "Наименование",
                "Количество",
                "Серийный номер",
            ]
        )

        # -------------------------------------------------
        # Размеры столбцов
        # -------------------------------------------------

        self.horizontalHeader().setStretchLastSection(
            False
        )

        self.horizontalHeader().setSectionResizeMode(
            self.NAME_COLUMN,
            QHeaderView.Stretch,
        )

        self.setColumnWidth(
            self.CATEGORY_COLUMN,
            130,
        )

        self.setColumnWidth(
            self.QUANTITY_COLUMN,
            90,
        )

        self.setColumnWidth(
            self.SERIAL_COLUMN,
            230,
        )

        # -------------------------------------------------
        # Редактирование
        # -------------------------------------------------

        self.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
        )

        self.setSelectionBehavior(
            QAbstractItemView.SelectItems
        )

        self.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.setAlternatingRowColors(
            True
        )

        self.verticalHeader().setVisible(
            False
        )

    # ---------------------------------------------------------

    def set_data(
        self,
        configuration: Configuration,
    ):

        self.setRowCount(
            0
        )

        for item in configuration.items:

            row = self.rowCount()

            self.insertRow(
                row
            )

            # -------------------------------------------------
            # Категория
            # -------------------------------------------------

            category_item = QTableWidgetItem(
                item.category.value
            )

            category_item.setFlags(
                category_item.flags()
                & ~Qt.ItemIsEditable
            )

            category_item.setTextAlignment(
                Qt.AlignLeft
                | Qt.AlignVCenter
            )

            self.setItem(
                row,
                self.CATEGORY_COLUMN,
                category_item,
            )

            # -------------------------------------------------
            # Наименование
            # -------------------------------------------------

            name_item = QTableWidgetItem(
                item.name
            )

            name_item.setFlags(
                name_item.flags()
                & ~Qt.ItemIsEditable
            )

            name_item.setTextAlignment(
                Qt.AlignLeft
                | Qt.AlignVCenter
            )

            self.setItem(
                row,
                self.NAME_COLUMN,
                name_item,
            )

            # -------------------------------------------------
            # Количество
            # -------------------------------------------------

            quantity_item = QTableWidgetItem(
                str(
                    item.quantity
                )
            )

            quantity_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.setItem(
                row,
                self.QUANTITY_COLUMN,
                quantity_item,
            )

            # -------------------------------------------------
            # Серийный номер
            # -------------------------------------------------

            serial_item = QTableWidgetItem(
                item.serial_number or ""
            )

            serial_item.setTextAlignment(
                Qt.AlignLeft
                | Qt.AlignVCenter
            )

            self.setItem(
                row,
                self.SERIAL_COLUMN,
                serial_item,
            )

    # ---------------------------------------------------------

    def get_quantities(
        self,
    ) -> dict:

        quantities = {}

        for row in range(
            self.rowCount()
        ):

            category_item = self.item(
                row,
                self.CATEGORY_COLUMN,
            )

            name_item = self.item(
                row,
                self.NAME_COLUMN,
            )

            quantity_item = self.item(
                row,
                self.QUANTITY_COLUMN,
            )

            if (
                category_item is None
                or name_item is None
                or quantity_item is None
            ):
                continue

            category = (
                category_item
                .text()
                .strip()
            )

            name = (
                name_item
                .text()
                .strip()
            )

            try:

                quantity = int(
                    quantity_item
                    .text()
                    .strip()
                )

            except ValueError:

                quantity = 1

            if quantity < 1:

                quantity = 1

            quantities[
                (
                    category,
                    name,
                )
            ] = quantity

        return quantities

    # ---------------------------------------------------------

    def get_serial_numbers(
        self,
    ) -> dict:
        """
        Возвращает серийные номера.

        Ключ:
            (категория, полное наименование)

        Значение:
            строка серийного номера.

        Для quantity > 1 можно пока вводить:

            SN001, SN002
        """

        serial_numbers = {}

        for row in range(
            self.rowCount()
        ):

            category_item = self.item(
                row,
                self.CATEGORY_COLUMN,
            )

            name_item = self.item(
                row,
                self.NAME_COLUMN,
            )

            serial_item = self.item(
                row,
                self.SERIAL_COLUMN,
            )

            if (
                category_item is None
                or name_item is None
                or serial_item is None
            ):
                continue

            key = (
                category_item.text().strip(),
                name_item.text().strip(),
            )

            serial_numbers[key] = (
                serial_item
                .text()
                .strip()
            )

        return serial_numbers

    # ---------------------------------------------------------

    def apply_to_configuration(
        self,
        configuration: Configuration,
    ):
        """
        Переносит из таблицы в Configuration:

        - количество;
        - серийный номер.

        После вызова configuration содержит
        именно те значения, которые пользователь
        видит в таблице.
        """

        quantities = (
            self.get_quantities()
        )

        serial_numbers = (
            self.get_serial_numbers()
        )

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

    # ---------------------------------------------------------

    def clear_serial_numbers(
        self,
    ):
        """
        Очищает только серийные номера.

        Состав и количества остаются.
        """

        for row in range(
            self.rowCount()
        ):

            serial_item = self.item(
                row,
                self.SERIAL_COLUMN,
            )

            if serial_item is not None:

                serial_item.setText(
                    ""
                )

    # ---------------------------------------------------------

    def focus_first_serial(
        self,
    ):
        """
        Ставит курсор в первый серийный номер.

        Удобно после создания предыдущего ПК:
        можно сразу начинать сканирование
        следующего комплекта.
        """

        if self.rowCount() == 0:
            return

        item = self.item(
            0,
            self.SERIAL_COLUMN,
        )

        if item is None:
            return

        self.setCurrentCell(
            0,
            self.SERIAL_COLUMN,
        )

        self.scrollToItem(
            item
        )

        self.editItem(
            item
        )

    # ---------------------------------------------------------

    def keyPressEvent(
        self,
        event,
    ):
        """
        Обрабатывает Enter от сканера.

        Если курсор находится в столбце
        серийного номера:

            Enter
              ↓
        следующая строка
              ↓
        сразу открывается ввод серийника.
        """

        if (
            event.key()
            in (
                Qt.Key_Return,
                Qt.Key_Enter,
            )
            and self.currentColumn()
            == self.SERIAL_COLUMN
        ):

            current_row = (
                self.currentRow()
            )

            # Сначала завершаем редактирование
            # текущей ячейки стандартным способом.

            super().keyPressEvent(
                event
            )

            next_row = (
                current_row + 1
            )

            if next_row < self.rowCount():

                next_item = self.item(
                    next_row,
                    self.SERIAL_COLUMN,
                )

                if next_item is not None:

                    self.setCurrentCell(
                        next_row,
                        self.SERIAL_COLUMN,
                    )

                    self.scrollToItem(
                        next_item
                    )

                    self.editItem(
                        next_item
                    )

            return

        super().keyPressEvent(
            event
        )
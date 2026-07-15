from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QVBoxLayout,
)

from models.label_model import LabelModel

from ui.additional_items_widget import AdditionalItemsWidget


class LabelEditorWidget(QGroupBox):

    label_changed = Signal(LabelModel)

    def __init__(self):
        super().__init__("Редактор изделия")

        self._model = LabelModel()

        root = QVBoxLayout(self)

        #
        # Комплектующие
        #

        hardware = QGroupBox("Комплектующие")

        layout = QFormLayout(hardware)

        self.model_name = QLineEdit()

        self.cpu = QLineEdit()
        self.ram = QLineEdit()
        self.storage = QLineEdit()
        self.gpu = QLineEdit()
        self.case = QLineEdit()
        self.psu = QLineEdit()

        layout.addRow("Модель", self.model_name)
        layout.addRow("CPU", self.cpu)
        layout.addRow("RAM", self.ram)
        layout.addRow("Storage", self.storage)
        layout.addRow("GPU", self.gpu)
        layout.addRow("Case", self.case)
        layout.addRow("PSU", self.psu)

        root.addWidget(hardware)

        #
        # Программное обеспечение
        #

        software = QGroupBox(
            "Программное обеспечение"
        )

        software_layout = QFormLayout(
            software
        )

        self.operating_system = QLineEdit()

        software_layout.addRow(
            "Операционная система",
            self.operating_system,
        )

        root.addWidget(software)

        #
        # Дополнительная комплектация
        #

        additional = QGroupBox(
            "Дополнительная комплектация"
        )

        additional_layout = QVBoxLayout(additional)

        self.additional_items = AdditionalItemsWidget()

        additional_layout.addWidget(
            self.additional_items
        )

        root.addWidget(additional)

        #
        # Сигналы
        #

        for field in (

            self.model_name,

            self.cpu,
            self.ram,
            self.storage,
            self.gpu,
            self.case,
            self.psu,

            self.operating_system,

        ):

            field.textEdited.connect(
                self._on_text_changed
            )

        self.additional_items.changed.connect(
            self._on_text_changed
        )

    # ---------------------------------------------------------

    def set_label(
        self,
        model,
    ):

        if model is None:
            raise RuntimeError(
                "LabelEditor получил None"
            )

        self._model = model

        self.model_name.setText(
            model.model_name
        )

        self.cpu.setText(model.cpu)
        self.ram.setText(model.ram)
        self.storage.setText(model.storage)
        self.gpu.setText(model.gpu)
        self.case.setText(model.case)
        self.psu.setText(model.psu)

        self.operating_system.setText(
            model.operating_system
        )

        self.additional_items.set_items(
            model.additional_items
        )

    # ---------------------------------------------------------

    def _on_text_changed(self):

        self._model.model_name = self.model_name.text()

        self._model.cpu = self.cpu.text()
        self._model.ram = self.ram.text()
        self._model.storage = self.storage.text()
        self._model.gpu = self.gpu.text()
        self._model.case = self.case.text()
        self._model.psu = self.psu.text()

        self._model.operating_system = (
            self.operating_system.text()
        )

        self._model.additional_items = (
            self.additional_items.items()
        )

        self.label_changed.emit(
            self._model
        )
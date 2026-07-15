from PySide6.QtWidgets import QWidget, QVBoxLayout

from models.label_model import LabelModel

from ui.document_options import DocumentOptions
from ui.label_editor import LabelEditorWidget
from ui.preview_widget import PreviewWidget


class PreviewPanel(QWidget):
    """
    Правая панель приложения.

    Содержит:

    - параметры документа;
    - предпросмотр;
    - редактор.
    """

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        #
        # Параметры документа
        #

        self.options = DocumentOptions()

        #
        # Предпросмотр
        #

        self.preview = PreviewWidget()

        #
        # Ручной редактор
        #

        self.editor = LabelEditorWidget()

        layout.addWidget(self.options)
        layout.addWidget(self.preview, 3)
        layout.addWidget(self.editor, 2)

        #
        # Синхронизация редактора
        #

        self.editor.label_changed.connect(
            self.preview.set_label
        )

    # ---------------------------------------------------------

    def set_label(
        self,
        label: LabelModel,
    ):

        self.preview.set_label(label)

        self.editor.set_label(label)

    # ---------------------------------------------------------

    def label(self) -> LabelModel:

        return self.editor._model

    # ---------------------------------------------------------

    def manufacturer(self):

        return self.options.selected_manufacturer()

    # ---------------------------------------------------------

    def layout_mode(self):

        return self.options.selected_layout()
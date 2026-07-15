from PySide6.QtWidgets import QFrame, QVBoxLayout


class BaseSectionWidget(QFrame):
    """
    Базовый класс для всех секций этикетки.
    """

    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.NoFrame)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
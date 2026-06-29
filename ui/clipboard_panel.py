from PySide6.QtWidgets import QTextEdit


class ClipboardPanel(QTextEdit):
    def __init__(self):
        super().__init__()

        self.setPlaceholderText(
            "Вставьте сюда текст спецификации из 1С\n\n"
            "или нажмите кнопку 'Вставить из буфера'."
        )

    def set_clipboard_text(self, text: str):
        self.setPlainText(text)
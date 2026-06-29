from PySide6.QtWidgets import QLabel, QStatusBar


class MainStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.article_label = QLabel("Артикул: —")
        self.serial_label = QLabel("Серийный №: —")
        self.date_label = QLabel("Дата: —")

        self.addPermanentWidget(self.article_label)
        self.addPermanentWidget(self.serial_label)
        self.addPermanentWidget(self.date_label)

    def set_article(self, article: str):
        self.article_label.setText(f"Артикул: {article}")

    def set_serial(self, serial: str):
        self.serial_label.setText(f"Серийный №: {serial}")

    def set_date(self, date: str):
        self.date_label.setText(f"Дата: {date}")
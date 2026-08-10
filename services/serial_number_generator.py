import json
from pathlib import Path


class SerialNumberGenerator:
    """
    Генератор производственных серийных номеров
    и артикулов.

    Формат серийного номера:
        2608292
        2608293
        2608294

    Формат артикула:
        101259
        101260
        101261
    """

    SERIAL_START = 2608291
    ARTICLE_START = 101258

    def __init__(self):

        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.file = self.data_dir / "serial_number.json"

    # --------------------------------------------------

    def next(self) -> str:

        data = self._load_data()

        serial = int(
            data.get(
                "serial",
                self.SERIAL_START,
            )
        )

        serial += 1

        data["serial"] = serial

        self._save_data(data)

        return str(serial)

    # --------------------------------------------------

    def current(self) -> str:

        data = self._load_data()

        serial = int(
            data.get(
                "serial",
                self.SERIAL_START,
            )
        )

        return str(serial)

    # --------------------------------------------------

    def next_article(self) -> str:

        data = self._load_data()

        article = int(
            data.get(
                "article",
                self.ARTICLE_START,
            )
        )

        article += 1

        data["article"] = article

        self._save_data(data)

        return str(article)

    # --------------------------------------------------

    def current_article(self) -> str:

        data = self._load_data()

        article = int(
            data.get(
                "article",
                self.ARTICLE_START,
            )
        )

        return str(article)

    # --------------------------------------------------

    def _load_data(self) -> dict:

        if not self.file.exists():

            return {
                "serial": self.SERIAL_START,
                "article": self.ARTICLE_START,
            }

        try:

            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:

            return {
                "serial": self.SERIAL_START,
                "article": self.ARTICLE_START,
            }

    # --------------------------------------------------

    def _save_data(
        self,
        data: dict,
    ):

        with open(self.file, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )
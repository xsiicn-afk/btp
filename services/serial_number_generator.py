import json
from datetime import datetime
from pathlib import Path


class SerialNumberGenerator:
    """
    Генератор серийных номеров.

    Формат:
        YYMMNNN

    Пример:
        2607001
        2607002
        2607003
    """

    def __init__(self):

        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.file = self.data_dir / "serial_number.json"

    def next(self) -> str:

        counter = self._load_counter()

        counter += 1

        self._save_counter(counter)

        prefix = datetime.now().strftime("%y%m")

        return f"{prefix}{counter:03d}"

    # --------------------------------------------------

    def current(self) -> str:

        counter = self._load_counter()

        prefix = datetime.now().strftime("%y%m")

        return f"{prefix}{counter:05d}"

    # --------------------------------------------------

    def _load_counter(self) -> int:

        if not self.file.exists():
            return 0

        try:

            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)

            return int(data.get("counter", 0))

        except Exception:
            return 0

    # --------------------------------------------------

    def _save_counter(self, counter: int):

        with open(self.file, "w", encoding="utf-8") as f:

            json.dump(
                {
                    "counter": counter
                },
                f,
                indent=4,
                ensure_ascii=False,
            )
from pathlib import Path
import tempfile

import qrcode


class QrService:

    def __init__(self):

        self.temp = Path(tempfile.gettempdir())

    # ---------------------------------------------------------

    def create_serial(self, serial: str) -> str:

        filename = self.temp / "serial_qr.png"

        image = qrcode.make(serial)

        image.save(filename)

        return str(filename)

    # ---------------------------------------------------------

    def create_article(self, article: int) -> str:

        filename = self.temp / "article_qr.png"

        image = qrcode.make(str(article))

        image.save(filename)

        return str(filename)
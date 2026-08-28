from pathlib import Path
import tempfile
from datetime import datetime

import qrcode
from openpyxl.drawing.image import Image as XLImage


class SpecificationWriter:

    MONTHS = {
        1: "янв", 2: "фев", 3: "мар",
        4: "апр", 5: "май", 6: "июн",
        7: "июл", 8: "авг", 9: "сен",
        10: "окт", 11: "ноя", 12: "дек",
    }

    def __init__(self, sheet):
        self.sheet = sheet

    # ---------------------------------------------------------

    def _cell(self, address):

        cell = self.sheet[address]

        if cell.__class__.__name__ != "MergedCell":
            return cell

        for merged in self.sheet.merged_cells.ranges:

            if address in merged:
                return self.sheet.cell(
                    merged.min_row,
                    merged.min_col,
                )

        return cell

    # ---------------------------------------------------------

    def write(self, label):

        self._write_header(label)
        self._write_components(label)

    # ---------------------------------------------------------

    def _format_date(self, value):

        if not value:
            return ""

        for fmt in ("%d.%m.%Y", "%Y-%m-%d"):

            try:
                dt = datetime.strptime(value, fmt)
                return f"{self.MONTHS[dt.month]} {dt.year}"
            except ValueError:
                pass

        return value

    # ---------------------------------------------------------

    def _write_header(self, label):

        self._cell("A1").value = label.model_name

        self._cell("C4").value = str(label.serial)

        self._cell("M4").value = label.article_code

        self._cell("W4").value = label.product_code or ""

        self._cell("AA6").value = self._format_date(label.date)

        # Шаблон открывается заново при каждой печати,
        # поэтому ничего не очищаем — заводские картинки
        # останутся на месте.

        self._insert_qr(
            str(label.serial),
            "H4",
        )

        if label.product_code:

            self._insert_qr(
                str(label.product_code),
                "R4",
            )

    # ---------------------------------------------------------

    def _insert_qr(
        self,
        value,
        cell,
    ):

        if not value:
            return

        temp_dir = Path(tempfile.gettempdir()) / "ByTopQR"
        temp_dir.mkdir(exist_ok=True)

        qr_path = temp_dir / f"{value}.png"

        qr = qrcode.QRCode(
            version=2,
            border=1,
            box_size=8,
        )

        qr.add_data(value)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        img.save(qr_path)

        picture = XLImage(str(qr_path))

        picture.width = 48
        picture.height = 48

        self.sheet.add_image(
            picture,
            cell,
        )

    # ---------------------------------------------------------

    def get_rows(self, label):

        rows = []

        for item in getattr(label, "items", []):

            name = (item.name or "").strip()

            if not name:
                continue

            rows.append(
                (
                    name,
                    max(1, int(item.quantity or 1)),
                )
            )

        return rows

    # ---------------------------------------------------------

    def _write_components(self, label):

        start_row = 8

        for index, (name, qty) in enumerate(
            self.get_rows(label),
            start=1,
        ):

            row = start_row + index - 1

            if row > 17:
                break

            self._cell(f"A{row}").value = index
            self._cell(f"B{row}").value = name
            self._cell(f"AA{row}").value = qty
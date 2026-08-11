from pathlib import Path
import tempfile

import barcode
from barcode.writer import ImageWriter

class SpecificationWriter:
    """
    Заполняет один блок производственной спецификации
    и добавляет штрихкод серийного номера.
    """
    # ---------------------------------------------------------

    def __init__(
        self,
        sheet=None,
        coordinates=None,
    ):

        self.sheet = sheet
        self.coords = coordinates or {}

    # ---------------------------------------------------------

    def write(
        self,
        label,
    ):

        self._write_header(label)
        self._write_components(label)

    # ---------------------------------------------------------

    def _write_header(
        self,
        label,
    ):

        c = self.coords

        self.sheet.Range(c["TITLE"]).Value = label.title
        self.sheet.Range(c["SERIAL"]).Value = label.serial
        self.sheet.Range(c["MODEL"]).Value = label.internal_name
        self.sheet.Range(c["ARTICLE"]).Value = label.article_code

        self.sheet.Range(c["DATE"]).Value = (
            f"ДАТА ПРОИЗВОДСТВА: {label.date}"
        )

        # ---------------------------------------------
        # Штрихкод серийного номера
        # ---------------------------------------------

        self._insert_serial_barcode(label.serial)

    # ---------------------------------------------------------

    def _insert_serial_barcode(
        self,
        serial: str,
    ):

        if not serial:
            return

        c = self.coords

        # -------------------------------------------------
        # Определяем позицию штрихкода по блоку спецификации
        # -------------------------------------------------

        first_component = c.get("FIRST_COMPONENT", "A1")

        row = int(
            "".join(filter(str.isdigit, first_component))
    )

        title_col = "".join(
            filter(str.isalpha, c.get("TITLE", "A1"))
    )

        # Верхний левый блок
        if row < 20 and title_col == "A":
            barcode_cell_name = "H4"

        # Верхний правый блок
        elif row < 20 and title_col == "AE":
            barcode_cell_name = "AL4"

        # Нижний левый блок
        elif row >= 20 and title_col == "A":
            barcode_cell_name = "H31"

        # Нижний правый блок
        else:
            barcode_cell_name = "AL31"

        barcode_cell = self.sheet.Range(barcode_cell_name)

        # -------------------------------------------------
        # Удаляем старые штрихкоды
        # -------------------------------------------------

        for shape in list(self.sheet.Shapes):

            try:
                if shape.Name.startswith("SN_BARCODE_"):
                    shape.Delete()
            except Exception:
                pass

        # -------------------------------------------------
        # Генерируем PNG Code128
        # -------------------------------------------------

        temp_dir = Path(tempfile.gettempdir()) / "ByTopBarcode"
        temp_dir.mkdir(exist_ok=True)

        barcode_path = temp_dir / f"{serial}.png"

        code128 = barcode.get(
            "code128",
            serial,
            writer=ImageWriter(),
    )

        code128.save(
            str(barcode_path.with_suffix("")),
            options={
                "module_width": 0.22,
                "module_height": 10,
                "write_text": False,   
                "quiet_zone": 1,
                "dpi": 300,
            },
    )

        # -------------------------------------------------
        # Вставляем изображение в нужную ячейку
        # -------------------------------------------------

        picture = self.sheet.Shapes.AddPicture(
            str(barcode_path),
            False,
            True,
            barcode_cell.Left + 2,
            barcode_cell.Top + 2,
            105,
            28,
    )

        picture.Name = f"SN_BARCODE_{serial}"

        # ---------------------------------------------------------

    def get_rows(
        self,
        label,
    ):

        rows = []

        items = getattr(label, "items", [])

        for item in items:

            name = (
                getattr(item, "name", "")
                or ""
            ).strip()

            if not name:
                continue

            quantity = getattr(item, "quantity", 1)

            try:
                quantity = int(quantity)
            except (TypeError, ValueError):
                quantity = 1

            if quantity < 1:
                quantity = 1

            rows.append((name, quantity))

        if not rows:

            component_fields = (
                "cpu",
                "cooler",
                "motherboard",
                "ram",
                "storage",
                "case",
                "psu",
                "gpu",
        )

            for field in component_fields:

                value = getattr(label, field, "")

                if value:
                    rows.append((value, 1))

            operating_system = getattr(label, "operating_system", "")

            if operating_system:
                rows.append((operating_system, 1))

        return rows

    # ---------------------------------------------------------

    def _write_components(
        self,
        label,
    ):

        c = self.coords

        first_component = c["FIRST_COMPONENT"]
        first_qty = c["FIRST_QTY"]

        component_column = "".join(filter(str.isalpha, first_component))
        qty_column = "".join(filter(str.isalpha, first_qty))

        row = int(
            "".join(filter(str.isdigit, first_component))
        )

        for name, quantity in self.get_rows(label):

            self.sheet.Range(f"{component_column}{row}").Value = name
            self.sheet.Range(f"{qty_column}{row}").Value = quantity

            row += 1

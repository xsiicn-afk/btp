from printing.layout_coordinates import (
    TOP_LEFT,
    TOP_RIGHT,
    BOTTOM_LEFT,
    BOTTOM_RIGHT,
)


class SpecificationWriter:
    """
    Заполняет спецификацию изделия.
    """

    BLOCKS = {
        "TOP_LEFT": TOP_LEFT,
        "TOP_RIGHT": TOP_RIGHT,
        "BOTTOM_LEFT": BOTTOM_LEFT,
        "BOTTOM_RIGHT": BOTTOM_RIGHT,
    }

    def __init__(
        self,
        sheet,
        block="TOP_LEFT",
    ):
        self.sheet = sheet
        self.coords = self.BLOCKS[block]

    # ---------------------------------------------------------

    def write(self, label):

        self.write_header(label)
        self.write_components(label)

    # ---------------------------------------------------------

    def write_header(self, label):

        c = self.coords

        self.sheet.Range(
            c["TITLE"]
        ).Value = label.title

        self.sheet.Range(
            c["SERIAL"]
        ).Value = label.serial

        self.sheet.Range(
            c["MODEL"]
        ).Value = label.internal_name

        self.sheet.Range(
            c["ARTICLE"]
        ).Value = label.article_code

        self.sheet.Range(
            c["DATE"]
        ).Value = (
            f"ДАТА ПРОИЗВОДСТВА: {label.date}"
        )

    # ---------------------------------------------------------

    def write_components(self, label):

        c = self.coords

        component_cell = c["FIRST_COMPONENT"]
        qty_cell = c["FIRST_QTY"]

        start_row = int(
            "".join(
                ch for ch in component_cell
                if ch.isdigit()
            )
        )

        component_column = "".join(
            ch for ch in component_cell
            if ch.isalpha()
        )

        qty_column = "".join(
            ch for ch in qty_cell
            if ch.isalpha()
        )

        row = start_row

        components = [

            label.cpu,
            label.cooler,
            label.motherboard,
            label.ram,
            label.storage,
            label.case,
            label.psu,
            label.gpu,

        ]

        for value in components:

            if not value:
                continue

            self.sheet.Range(
                f"{component_column}{row}"
            ).Value = value

            self.sheet.Range(
                f"{qty_column}{row}"
            ).Value = 1

            row += 1

        if label.operating_system:

            self.sheet.Range(
                f"{component_column}{row}"
            ).Value = label.operating_system

            self.sheet.Range(
                f"{qty_column}{row}"
            ).Value = 1

            row += 1

        for item in label.additional_items:

            self.sheet.Range(
                f"{component_column}{row}"
            ).Value = item.name

            self.sheet.Range(
                f"{qty_column}{row}"
            ).Value = item.quantity

            row += 1
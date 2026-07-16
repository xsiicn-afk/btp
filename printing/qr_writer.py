from pathlib import Path


class QrWriter:
    """
    Вставка QR-кодов в Excel.
    """

    BLOCKS = {

        "TOP_LEFT": {

            "SERIAL": ("H4", "J6"),
            "ARTICLE": ("R4", "T6"),

        },

        "TOP_RIGHT": {

            "SERIAL": ("AL4", "AN6"),
            "ARTICLE": ("BD4", "BF6"),

        },

        "BOTTOM_LEFT": {

            "SERIAL": ("H31", "J33"),
            "ARTICLE": ("R31", "T33"),

        },

        "BOTTOM_RIGHT": {

            "SERIAL": ("AL31", "AN33"),
            "ARTICLE": ("BD31", "BF33"),

        },

    }

    def __init__(
        self,
        sheet,
        block="TOP_LEFT",
    ):

        self.sheet = sheet
        self.coords = self.BLOCKS[block]

    # ---------------------------------------------------------

    def insert(
        self,
        filename: str,
        left_cell: str,
        right_cell: str,
    ):

        left = self.sheet.Range(left_cell)
        right = self.sheet.Range(right_cell)

        x = left.Left
        y = left.Top

        width = (
            right.Left
            + right.Width
            - left.Left
        )

        height = (
            right.Top
            + right.Height
            - left.Top
        )

        self.sheet.Shapes.AddPicture(
            str(Path(filename).resolve()),
            False,
            True,
            x,
            y,
            width,
            height,
        )

    # ---------------------------------------------------------

    def serial(
        self,
        filename,
    ):

        left, right = self.coords["SERIAL"]

        self.insert(
            filename,
            left,
            right,
        )

    # ---------------------------------------------------------

    def article(
        self,
        filename,
    ):

        left, right = self.coords["ARTICLE"]

        self.insert(
            filename,
            left,
            right,
        )
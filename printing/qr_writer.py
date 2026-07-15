from pathlib import Path


class QrWriter:
    """
    Вставка QR-кодов в Excel.
    """

    def __init__(self, sheet):

        self.sheet = sheet

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

    def serial(self, filename):

        self.insert(
            filename,
            "H4",
            "J6",
        )

    # ---------------------------------------------------------

    def article(self, filename):

        self.insert(
            filename,
            "R4",
            "T6",
        )
from openpyxl.utils.cell import (
    coordinate_from_string,
    column_index_from_string,
    get_column_letter,
)


class CellMapper:
    """
    Преобразует координаты Excel
    с учетом смещения блока.
    """

    def __init__(
        self,
        row_offset: int = 0,
        col_offset: int = 0,
    ):

        self.row_offset = row_offset
        self.col_offset = col_offset

    # ---------------------------------------------------------

    def cell(
        self,
        coordinate: str,
    ) -> str:

        column, row = coordinate_from_string(
            coordinate
        )

        column = (
            column_index_from_string(column)
            + self.col_offset
        )

        row += self.row_offset

        return (
            f"{get_column_letter(column)}{row}"
        )
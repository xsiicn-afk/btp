"""
Координаты производственной спецификации.

Описывается только один базовый блок.
Координаты остальных блоков вычисляются автоматически.

Позиции на листе:

    1 | 2
    -----
    3 | 4
"""

from openpyxl.utils.cell import (
    coordinate_from_string,
    column_index_from_string,
    get_column_letter,
)

# ---------------------------------------------------------
# Координаты базового блока
# ---------------------------------------------------------

BASE_LAYOUT = {

    "TITLE": "A1",

    "SERIAL": "C4",

    "MODEL": "M4",

    "ARTICLE": "W4",

    "DATE": "U6",

    "FIRST_COMPONENT": "B8",

    "FIRST_QTY": "AB8",

}

# ---------------------------------------------------------
# Смещения блоков
#
# Номер позиции -> (смещение строк, смещение столбцов)
# ---------------------------------------------------------

OFFSETS = {

    1: (0, 0),

    2: (0, 30),

    3: (27, 0),

    4: (27, 30),

}

# ---------------------------------------------------------
# Области печати каждой позиции
# ---------------------------------------------------------

PRINT_AREAS = {

    1: ("A", 1, "AC", 26),

    2: ("AE", 1, "BG", 26),

    3: ("A", 28, "AC", 53),

    4: ("AE", 28, "BG", 53),

}

# ---------------------------------------------------------


def shift_cell(
    cell: str,
    row_offset: int,
    column_offset: int,
) -> str:

    column, row = coordinate_from_string(cell)

    column = (
        column_index_from_string(column)
        + column_offset
    )

    row += row_offset

    return f"{get_column_letter(column)}{row}"


# ---------------------------------------------------------


def get_layout(
    position: int,
) -> dict[str, str]:

    if position not in OFFSETS:

        raise ValueError(
            f"Неизвестная позиция: {position}"
        )

    row_offset, column_offset = OFFSETS[position]

    layout = {}

    for key, cell in BASE_LAYOUT.items():

        layout[key] = shift_cell(
            cell,
            row_offset,
            column_offset,
        )

    return layout


# ---------------------------------------------------------
def get_print_area(
    positions: list[int],
) -> str:
    """
    Возвращает минимальную область печати,
    содержащую все выбранные позиции.
    """

    if not positions:

        raise ValueError(
            "Список позиций пуст."
        )

    selected = []

    for position in positions:

        if position not in PRINT_AREAS:

            raise ValueError(
                f"Неизвестная позиция: {position}"
            )

        selected.append(
            PRINT_AREAS[position]
        )

    left = min(
        area[0]
        for area in selected
    )

    top = min(
        area[1]
        for area in selected
    )

    right = max(
        area[2]
        for area in selected
    )

    bottom = max(
        area[3]
        for area in selected
    )

    return (
        f"${left}${top}:${right}${bottom}"
    )
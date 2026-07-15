from datetime import datetime


MONTHS = {

    1: "ЯНВАРЬ",
    2: "ФЕВРАЛЬ",
    3: "МАРТ",
    4: "АПРЕЛЬ",
    5: "МАЙ",
    6: "ИЮНЬ",
    7: "ИЮЛЬ",
    8: "АВГУСТ",
    9: "СЕНТЯБРЬ",
    10: "ОКТЯБРЬ",
    11: "НОЯБРЬ",
    12: "ДЕКАБРЬ",

}


def production_date(date_string: str) -> str:
    """
    Преобразует

    14.07.2026

    →

    ИЮЛЬ 2026 г.
    """

    if not date_string:
        return ""

    try:

        date = datetime.strptime(
            date_string,
            "%d.%m.%Y",
        )

    except ValueError:

        return date_string

    month = MONTHS.get(
        date.month,
        "",
    )

    return f"{month} {date.year} г."
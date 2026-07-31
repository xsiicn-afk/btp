from printing.date_formatter import production_date
from printing.manufacturer_data import ManufacturerInfo


class AddressWriter:
    """
    Заполняет адресные наклейки в указанных блоках.

    Writer ничего не знает о LabelModel, PageLayout и количестве
    спецификаций на странице. Он просто получает список блоков,
    которые необходимо заполнить.
    """

    BLOCKS = {
        "TOP_RIGHT": (
            "AE4",
            "AE9",
            "AE11",
            "AE24",
        ),
        "BOTTOM_LEFT": (
            "A31",
            "A36",
            "A38",
            "A51",
        ),
        "BOTTOM_RIGHT": (
            "AE31",
            "AE36",
            "AE38",
            "AE51",
        ),
    }

    def __init__(self, sheet):

        self.sheet = sheet

    # ---------------------------------------------------------

    def write(
        self,
        blocks: list[str],
        manufacturer: ManufacturerInfo,
        date,
    ):

        production = production_date(date)

        for block in blocks:

            if block not in self.BLOCKS:
                continue

            title, tu, address, production_cell = self.BLOCKS[block]

            self.sheet.Range(title).Value = manufacturer.title
            self.sheet.Range(tu).Value = manufacturer.tu
            self.sheet.Range(address).Value = manufacturer.address
            self.sheet.Range(production_cell).Value = production
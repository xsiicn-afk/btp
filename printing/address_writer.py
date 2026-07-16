from models.page_layout import PageLayout

from printing.date_formatter import production_date
from printing.manufacturer_data import get_manufacturer_info


class AddressWriter:
    """
    Заполняет свободные адресные наклейки.
    """

    BLOCKS = (

        ("AE4", "AE9", "AE11", "AE24"),

        ("A31", "A36", "A38", "A51"),

        ("AE31", "AE36", "AE38", "AE51"),

    )

    def __init__(self, sheet):

        self.sheet = sheet

    # ---------------------------------------------------------

    def write(self, label):

        info = get_manufacturer_info(
            label.manufacturer,
        )

        date = production_date(
            label.date,
        )

        #
        # Сколько адресов печатаем
        #

        if label.layout == PageLayout.ONE_SPEC_THREE_ADDRESS:

            blocks = 3

        elif label.layout == PageLayout.TWO_SPEC_TWO_ADDRESS:

            blocks = 2

        elif label.layout == PageLayout.THREE_SPEC_ONE_ADDRESS:

            blocks = 1

        else:

            blocks = 0

        #
        # Заполняем нужное количество
        #

        for title, tu, address, production in self.BLOCKS[:blocks]:

            self.sheet.Range(title).Value = info.title

            self.sheet.Range(tu).Value = info.tu

            self.sheet.Range(address).Value = info.address

            self.sheet.Range(
                production
            ).Value = date
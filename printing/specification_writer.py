class SpecificationWriter:
    """
    Заполняет спецификацию изделия.
    """

    def __init__(self, sheet):
        self.sheet = sheet

    # ---------------------------------------------------------

    def write(self, label):

        self.write_header(label)

        self.write_components(label)

    # ---------------------------------------------------------

    def write_header(self, label):

        self.sheet.Range("A1").Value = label.title

        self.sheet.Range("C4").Value = label.serial

        self.sheet.Range("M4").Value = label.internal_name

        self.sheet.Range("W4").Value = label.article_code

        self.sheet.Range(
            "U6"
        ).Value = (
            f"ДАТА ПРОИЗВОДСТВА: {label.date}"
        )

    # ---------------------------------------------------------

    def write_components(self, label):

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

        row = 8

        for value in components:

            self.sheet.Range(
                f"B{row}"
            ).Value = value or ""

            self.sheet.Range(
                f"AB{row}"
            ).Value = 1

            row += 1
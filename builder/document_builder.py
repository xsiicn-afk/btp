from models.configuration import Configuration
from models.category import Category
from models.label_document import LabelDocument, LabelRow


class DocumentBuilder:
    """
    Преобразует Configuration в печатный документ.
    """

    def build(self, configuration: Configuration) -> LabelDocument:

        document = LabelDocument()

        document.title = configuration.model_name
        document.serial = configuration.serial
        document.article = configuration.article
        document.production_date = configuration.date

        row_number = 1

        category_order = (
            Category.CPU,
            Category.COOLER,
            Category.MOTHERBOARD,
            Category.RAM,
            Category.STORAGE,
            Category.GPU,
            Category.CASE,
            Category.PSU,
            Category.OS,
        )

        for category in category_order:

            for item in configuration.get_items(category):

                document.rows.append(
                    LabelRow(
                        number=row_number,
                        name=item.name,
                        quantity=item.quantity,
                    )
                )

                row_number += 1

        return document
from models.manufacturer import Manufacturer


class ManufacturerService:

    DATA = {

        Manufacturer.EPICA: {

            "title": "ООО «ЭпикумЛаб»",

            "address": (
                "344064, Ростовская область, "
                "г. Ростов-на-Дону, "
                "пер. Радиаторный, 9А"
            ),

            "phone": "+7 (863) 000-00-00",

            "email": "info@epicumlab.ru",

        },

        Manufacturer.AXUS: {

            "title": "ООО «Аксус»",

            "address": (
                "344064, Ростовская область, "
                "г. Ростов-на-Дону, "
                "пер. Радиаторный, 9А"
            ),

            "phone": "+7 (863) 000-00-00",

            "email": "info@axus.ru",

        },

    }

    # ---------------------------------------------------------

    @classmethod
    def get(
        cls,
        manufacturer: Manufacturer,
    ):

        return cls.DATA[manufacturer]
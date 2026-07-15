from dataclasses import dataclass

from models.manufacturer import Manufacturer


@dataclass(frozen=True)
class ManufacturerInfo:

    title: str
    tu: str
    address: str


EPICA = ManufacturerInfo(

    title="Системный блок ЭпикумЛаб",

    tu="ТУ 26.20.13-001-93871549-2026",

    address=(
        'ООО "Эпика".\n'
        "344037, РФ, Ростовская область,\n"
        "г. Ростов-на-Дону, ул. 14-я линия, д. 86.\n"
        "тел. +7 (863) 283-86-90\n"
        "e-mail: info@epica-group.ru"
    ),
)


AXUS = ManufacturerInfo(

    title="Системный блок ByTop",

    tu="ТУ 26.20.15-003-60270195-2023",

    address=(
        'ООО "АКСУС".\n'
        "344037, РФ, Самарская область,\n"
        "г. Самара, ул. Партизанская, д. 86, пом. 101/1\n"
        "тел. +7 (846) 277-01-03\n"
        "e-mail: axus-samara@axusgroup.ru"
    ),
)


def get_manufacturer_info(
    manufacturer: Manufacturer,
) -> ManufacturerInfo:

    if manufacturer == Manufacturer.AXUS:
        return AXUS

    return EPICA
from enum import Enum


class Category(Enum):
    CPU = "cpu"
    MOTHERBOARD = "motherboard"
    COOLER = "cooler"
    RAM = "ram"
    STORAGE = "storage"
    GPU = "gpu"
    PSU = "psu"
    CASE = "case"
    OS = "os"
    OTHER = "other"
from models.category import Category
from models.configuration import Configuration
from models.label_model import LabelModel

from builder.cpu_builder import CpuBuilder


class ModelBuilder:
    """Преобразует Configuration в LabelModel."""

    def __init__(self):
        self.cpu_builder = CpuBuilder()

    def build(self, configuration: Configuration) -> LabelModel:

        label = LabelModel()

        label.title = configuration.model_name
        label.serial = configuration.serial
        label.article = configuration.article
        label.date = configuration.date

        cpu = configuration.get_items(Category.CPU)
        if cpu:
            label.cpu = self.cpu_builder.build(cpu[0].name)

        motherboard = configuration.get_items(Category.MOTHERBOARD)
        if motherboard:
            label.motherboard = motherboard[0].name

        cooler = configuration.get_items(Category.COOLER)
        if cooler:
            label.cooler = cooler[0].name

        ram = configuration.get_items(Category.RAM)
        if ram:
            label.ram = ram[0].name

        storage = configuration.get_items(Category.STORAGE)
        if storage:
            label.storage = storage[0].name

        gpu = configuration.get_items(Category.GPU)
        if gpu:
            label.gpu = gpu[0].name

        case = configuration.get_items(Category.CASE)
        if case:
            label.case = case[0].name

        psu = configuration.get_items(Category.PSU)
        if psu:
            label.psu = psu[0].name

        return label
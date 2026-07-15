from models.category import Category
from models.configuration import Configuration
from models.label_model import LabelModel

from builder.cpu_builder import CpuBuilder
from builder.ram_builder import RamBuilder
from builder.gpu_builder import GpuBuilder
from builder.storage_builder import StorageBuilder
from builder.model_name_builder import ModelNameBuilder
from builder.psu_builder import PsuBuilder
from builder.case_builder import CaseBuilder

class ModelBuilder:
    """Преобразует Configuration в LabelModel."""

    def __init__(self):
        self.gpu_builder = GpuBuilder()
        self.cpu_builder = CpuBuilder()
        self.ram_builder = RamBuilder()
        self.storage_builder = StorageBuilder()
        self.model_name_builder = ModelNameBuilder()
        self.psu_builder = PsuBuilder()
        self.case_builder = CaseBuilder()
    def build(self, configuration: Configuration) -> LabelModel:

        label = LabelModel()

        label.serial = configuration.serial
        label.article = configuration.article
        label.date = configuration.date
        label.operating_system = (
            configuration.operating_system
        )
        # CPU
        cpu = configuration.get_items(Category.CPU)
        if cpu:
            label.cpu = self.cpu_builder.build(cpu[0].name)

        # Материнская плата
        motherboard = configuration.get_items(Category.MOTHERBOARD)
        if motherboard:
            label.motherboard = motherboard[0].name

        # Кулер
        cooler = configuration.get_items(Category.COOLER)
        if cooler:
            label.cooler = cooler[0].name

        # RAM
        ram = configuration.get_items(Category.RAM)
        if ram:
            label.ram = self.ram_builder.build(
                ram[0].name,
                ram[0].quantity
            )

        # Накопитель
        storage = configuration.get_items(Category.STORAGE)
        if storage:
            label.storage = self.storage_builder.build(
                storage[0].name
            )

        # GPU
        gpu = configuration.get_items(Category.GPU)
        if gpu:
            label.gpu = self.gpu_builder.build(
                gpu[0].name
            )

        # Корпус
        case = configuration.get_items(Category.CASE)
        if case:
            label.case = self.case_builder.build(
                case[0].name
            )

        # Блок питания
        psu = configuration.get_items(Category.PSU)
        if psu:
            label.psu = self.psu_builder.build(
                psu[0].name
            )

        # Коммерческое название модели
        label.model_name = self.model_name_builder.build(
            label.cpu,
            label.ram,
            label.storage,
            label.gpu,
            label.case,
            label.psu,
        )

        return label
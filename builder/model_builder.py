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
    """
    Преобразует Configuration в LabelModel.
    """

    def __init__(self):

        self.gpu_builder = GpuBuilder()

        self.cpu_builder = CpuBuilder()

        self.ram_builder = RamBuilder()

        self.storage_builder = StorageBuilder()

        self.model_name_builder = (
            ModelNameBuilder()
        )

        self.psu_builder = PsuBuilder()

        self.case_builder = CaseBuilder()

    # ---------------------------------------------------------

    def build(
        self,
        configuration: Configuration,
    ) -> LabelModel:

        label = LabelModel()

        # -------------------------------------------------
        # Основные данные
        # -------------------------------------------------

        label.serial = (
            configuration.serial
        )

        label.article = (
            configuration.article
        )

        label.date = (
            configuration.date
        )

        # -------------------------------------------------
        # Сохраняем исходные позиции.
        #
        # Пока используем тот же список объектов Item.
        # Это позволит передать серийники комплектующих
        # дальше в BuildService / историю.
        # -------------------------------------------------

        label.items = list(
            configuration.items
        )

        # -------------------------------------------------
        # Операционная система
        # -------------------------------------------------

        label.operating_system = (
            configuration.operating_system
        )

        # -------------------------------------------------
        # CPU
        # -------------------------------------------------

        cpu = configuration.get_items(
            Category.CPU
        )

        if cpu:

            label.cpu = (
                self.cpu_builder.build(
                    cpu[0].name
                )
            )

        # -------------------------------------------------
        # Материнская плата
        # -------------------------------------------------

        motherboard = (
            configuration.get_items(
                Category.MOTHERBOARD
            )
        )

        if motherboard:

            label.motherboard = (
                motherboard[0].name
            )

        # -------------------------------------------------
        # Кулер
        # -------------------------------------------------

        cooler = configuration.get_items(
            Category.COOLER
        )

        if cooler:

            label.cooler = (
                cooler[0].name
            )

        # -------------------------------------------------
        # RAM
        # -------------------------------------------------

        ram = configuration.get_items(
            Category.RAM
        )

        if ram:

            label.ram = (
                self.ram_builder.build(
                    ram[0].name,
                    ram[0].quantity,
                )
            )

        # -------------------------------------------------
        # Накопители
        #
        # Раньше использовался только storage[0].
        #
        # Теперь обрабатываем ВСЕ накопители.
        # -------------------------------------------------

        storage_items = (
            configuration.get_items(
                Category.STORAGE
            )
        )

        storage_parts = []

        for storage_item in storage_items:

            storage_name = (
                self.storage_builder.build(
                    storage_item.name
                )
            )

            if not storage_name:
                continue

            # ---------------------------------------------
            # Если одинаковая товарная позиция имеет
            # количество больше одного:
            #
            # SSD NVMe 1TB x2
            # ---------------------------------------------

            if storage_item.quantity > 1:

                storage_name = (
                    f"{storage_name} "
                    f"x{storage_item.quantity}"
                )

            storage_parts.append(
                storage_name
            )

        # ModelNameBuilder уже разделяет основные
        # характеристики символом "/".
        #
        # Поэтому несколько накопителей также
        # объединяем через "/".

        label.storage = "/".join(
            storage_parts
        )

        # -------------------------------------------------
        # GPU
        # -------------------------------------------------

        gpu = configuration.get_items(
            Category.GPU
        )

        if gpu:

            label.gpu = (
                self.gpu_builder.build(
                    gpu[0].name
                )
            )

        # -------------------------------------------------
        # Корпус
        # -------------------------------------------------

        case = configuration.get_items(
            Category.CASE
        )

        if case:

            label.case = (
                self.case_builder.build(
                    case[0].name
                )
            )

        # -------------------------------------------------
        # Блок питания
        # -------------------------------------------------

        psu = configuration.get_items(
            Category.PSU
        )

        if psu:

            label.psu = (
                self.psu_builder.build(
                    psu[0].name
                )
            )

        # -------------------------------------------------
        # Коммерческое название компьютера
        # -------------------------------------------------

        label.model_name = (
            self.model_name_builder.build(
                label.cpu,
                label.ram,
                label.storage,
                label.gpu,
                label.case,
                label.psu,
                label.operating_system,
            )
        )

        return label
from datetime import datetime

from builder.model_builder import ModelBuilder

from models.configuration import Configuration
from models.label_model import LabelModel

from services.serial_number_generator import SerialNumberGenerator
from services.article_service import ArticleService
from services.build_history_service import BuildHistoryService
from services.user_service import UserService


class BuildService:
    """
    Создание производственного LabelModel.
    """

    def __init__(self):

        self.model_builder = ModelBuilder()

        self.serial_generator = SerialNumberGenerator()

        self.article_service = ArticleService()

        self.history = BuildHistoryService()

        self.user_service = UserService()

    # ---------------------------------------------------------

    def preview(
        self,
        configuration: Configuration,
    ) -> LabelModel:

        label = self.model_builder.build(configuration)

        label.date = datetime.now().strftime("%d.%m.%Y")

        # Берём код продукции из парсера.
        label.product_code = getattr(
            configuration,
            "product_code",
            "",
        )

        return label

    # ---------------------------------------------------------

    def create(
        self,
        configuration: Configuration,
        model_name: str = "",
        warranty_months: int = 36,
    ) -> LabelModel:
        """
        Создаёт изделие и сохраняет его в БД.
        """

        label = self.model_builder.build(configuration)

        # -------------------------------------------------
        # Ручное название
        # -------------------------------------------------

        manual_model_name = (
            model_name.strip()
            if model_name
            else ""
        )

        if manual_model_name:
            label.model_name = manual_model_name

        if not label.model_name:
            label.model_name = "Системный блок"

        # -------------------------------------------------
        # Гарантия
        # -------------------------------------------------

        try:
            warranty_months = int(warranty_months)
        except (TypeError, ValueError):
            warranty_months = 36

        if warranty_months < 0:
            warranty_months = 0

        label.warranty_months = warranty_months

        # -------------------------------------------------
        # Серийный номер
        # -------------------------------------------------

        label.serial = self.serial_generator.next()

        # -------------------------------------------------
        # Код продукции
        # -------------------------------------------------

        label.product_code = getattr(
            configuration,
            "product_code",
            "",
        )

        # -------------------------------------------------
        # Дата производства
        # -------------------------------------------------

        label.date = datetime.now().strftime("%d.%m.%Y")

        # -------------------------------------------------
        # Сигнатура модели
        # -------------------------------------------------

        signature = "|".join(
            [
                label.cpu or "",
                label.motherboard or "",
                label.cooler or "",
                label.ram or "",
                label.storage or "",
                label.gpu or "",
                label.case or "",
                label.psu or "",
                label.operating_system or "",
            ]
        )

        final_model_name = label.model_name
        internal_name = final_model_name

        # -------------------------------------------------
        # Артикул
        # -------------------------------------------------

        label.article_code = self.article_service.get_or_create(
            signature,
            final_model_name,
            internal_name,
        )

        # -------------------------------------------------
        # Пользователь
        # -------------------------------------------------

        label.created_by = self.user_service.current_user

        # -------------------------------------------------
        # Сохранение
        # -------------------------------------------------

        self.history.save(label)

        print(
            f"CREATE: {label.serial} ({self.user_service.current_user})"
        )

        return label
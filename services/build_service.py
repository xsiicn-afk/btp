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
        """
        Предпросмотр после Ctrl+V.

        Серийный номер и код модели
        пока не создаются.
        """

        label = self.model_builder.build(configuration)

        label.date = datetime.now().strftime("%d.%m.%Y")

        return label

    # ---------------------------------------------------------

    def create(
        self,
        configuration: Configuration,
    ) -> LabelModel:
        """
        Создание изделия.
        """

        label = self.model_builder.build(configuration)

        #
        # Серийный номер
        #

        label.serial = self.serial_generator.next()

        label.date = datetime.now().strftime("%d.%m.%Y")

        #
        # Сигнатура модели
        #

        signature = "|".join(
            [
                label.cpu,
                label.motherboard,
                label.cooler,
                label.ram,
                label.storage,
                label.gpu,
                label.case,
                label.psu,
            ]
        )

        #
        # Внутреннее название модели
        #

        model_name = label.model_name or label.title

        internal_name = (
            label.internal_name
            or model_name
        )

        #
        # Получаем код модели
        #

        label.article_code = self.article_service.get_or_create(
            signature,
            model_name,
            internal_name,
        )

        #
        # Временно сохраняем автора создания.
        # В следующем этапе это поле будет
        # записываться в базу данных.
        #

        label.created_by = self.user_service.current_user

        #
        # Сохраняем сборку
        #

        self.history.save(label)

        print(
            f"CREATE: {label.serial} "
            f"({self.user_service.current_user})"
        )

        return label
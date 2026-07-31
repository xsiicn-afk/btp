from datetime import datetime

from database.database import Database

from models.category import Category
from models.item import Item
from models.label_model import LabelModel

from printing.print_engine import PrintEngine

from services.user_service import UserService


class BuildHistoryService:

    def __init__(self):

        self.db = Database()

        self.user_service = UserService()

        self.printer = PrintEngine()

    # ---------------------------------------------------------

    def cursor(self):

        return self.db.cursor()

    # ---------------------------------------------------------

    def commit(self):

        self.db.commit()

    # ---------------------------------------------------------

    def save(
        self,
        label: LabelModel,
    ):

        """
        Сохраняет созданное изделие.

        Основная информация сохраняется
        в builds.

        Полный состав и серийные номера
        комплектующих сохраняются в build_items.
        """

        cursor = self.cursor()

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        model_name = (
            label.model_name
            or "Системный блок"
        )

        internal_name = model_name
        title = model_name

        warranty_months = getattr(
            label,
            "warranty_months",
            36,
        )

        try:

            warranty_months = int(
                warranty_months
            )

        except (
            TypeError,
            ValueError,
        ):

            warranty_months = 36

        try:

            # =================================================
            # Основная запись изделия
            # =================================================

            cursor.execute(
                """
                INSERT INTO builds(

                    serial,
                    article_code,
                    internal_name,
                    title,

                    model_name,
                    operating_system,
                    warranty_months,

                    cpu,
                    motherboard,
                    cooler,
                    ram,
                    storage,
                    gpu,
                    pc_case,
                    psu,

                    build_date,
                    created_at,
                    created_by,
                    version,

                    spec_printed,
                    passport_printed,
                    sticker_printed,
                    deleted

                )

                VALUES(

                    ?, ?, ?, ?,

                    ?, ?, ?,

                    ?, ?, ?, ?, ?, ?, ?, ?,

                    ?, ?, ?, ?,

                    ?, ?, ?, ?

                )
                """,
                (
                    label.serial,
                    label.article_code,
                    internal_name,
                    title,

                    model_name,
                    label.operating_system,
                    warranty_months,

                    label.cpu,
                    label.motherboard,
                    label.cooler,
                    label.ram,
                    label.storage,
                    label.gpu,
                    label.case,
                    label.psu,

                    label.date,
                    now,
                    self.user_service.current_user,
                    1,

                    0,
                    0,
                    0,
                    0,
                ),
            )

            # =================================================
            # Комплектующие
            # =================================================

            self._save_items(
                cursor,
                label,
            )

            self.commit()

        except Exception:

            self.db.rollback()

            raise

    # ---------------------------------------------------------

    def _save_items(
        self,
        cursor,
        label: LabelModel,
    ):

        if not label.items:

            return

        for item in label.items:

            category = item.category

            if hasattr(
                category,
                "value",
            ):

                category = category.value

            cursor.execute(
                """
                INSERT INTO build_items(

                    build_serial,
                    category,
                    name,
                    quantity,
                    serial_number

                )

                VALUES(

                    ?, ?, ?, ?, ?

                )
                """,
                (
                    label.serial,
                    str(category),
                    item.name,
                    item.quantity,
                    item.serial_number or "",
                ),
            )

            # ---------------------------------------------
            # Сразу запоминаем ID созданной строки.
            # ---------------------------------------------

            item.db_id = (
                cursor.lastrowid
            )

    # ---------------------------------------------------------

    def update_item_serial(
        self,
        item_id: int,
        serial_number: str,
    ) -> bool:
        """
        Изменяет серийный номер конкретной
        позиции уже созданного изделия.

        Используется карточкой изделия.
        """

        if item_id is None:

            return False

        serial_number = (
            serial_number
            or ""
        ).strip()

        cursor = self.cursor()

        try:

            cursor.execute(
                """
                UPDATE build_items

                SET serial_number = ?

                WHERE id = ?
                """,
                (
                    serial_number,
                    int(item_id),
                ),
            )

            self.commit()

            return (
                cursor.rowcount > 0
            )

        except Exception:

            self.db.rollback()

            raise

    # ---------------------------------------------------------

    def all(self):

        cursor = self.cursor()

        cursor.execute(
            """
            SELECT *

            FROM builds

            WHERE deleted = 0

            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    # ---------------------------------------------------------

    def load_label(
        self,
        serial: str,
    ) -> LabelModel | None:

        cursor = self.cursor()

        cursor.execute(
            """
            SELECT *

            FROM builds

            WHERE serial = ?
            """,
            (serial,),
        )

        row = cursor.fetchone()

        if row is None:

            return None

        label = LabelModel()

        # =====================================================
        # Основные данные
        # =====================================================

        label.serial = (
            row["serial"]
            or ""
        )

        # -----------------------------------------------------
        # Артикул
        # -----------------------------------------------------

        if "article_code" in row.keys():

            label.article_code = (
                row["article_code"]
                or 0
            )

        # -----------------------------------------------------
        # Название модели
        # -----------------------------------------------------

        if (
            "model_name" in row.keys()
            and row["model_name"]
        ):

            label.model_name = (
                row["model_name"]
            )

        elif (
            "title" in row.keys()
            and row["title"]
        ):

            label.model_name = (
                row["title"]
            )

        else:

            label.model_name = ""

        # -----------------------------------------------------
        # Операционная система
        # -----------------------------------------------------

        if "operating_system" in row.keys():

            label.operating_system = (
                row["operating_system"]
                or ""
            )

        # -----------------------------------------------------
        # Гарантия
        # -----------------------------------------------------

        if "warranty_months" in row.keys():

            value = row[
                "warranty_months"
            ]

            label.warranty_months = (
                value
                if value is not None
                else 36
            )

        else:

            label.warranty_months = 36

        # =====================================================
        # Характеристики
        # =====================================================

        label.cpu = (
            row["cpu"]
            or ""
        )

        label.motherboard = (
            row["motherboard"]
            or ""
        )

        label.cooler = (
            row["cooler"]
            or ""
        )

        label.ram = (
            row["ram"]
            or ""
        )

        label.storage = (
            row["storage"]
            or ""
        )

        label.gpu = (
            row["gpu"]
            or ""
        )

        label.case = (
            row["pc_case"]
            or ""
        )

        label.psu = (
            row["psu"]
            or ""
        )

        label.date = (
            row["build_date"]
            or ""
        )

        # =====================================================
        # Служебные данные
        # =====================================================

        if "created_by" in row.keys():

            label.created_by = (
                row["created_by"]
                or ""
            )

        if "version" in row.keys():

            label.version = (
                row["version"]
                or 1
            )

        # -----------------------------------------------------
        # Статусы печати
        # -----------------------------------------------------

        if "spec_printed" in row.keys():

            label.spec_printed = bool(
                row["spec_printed"]
            )

        if "passport_printed" in row.keys():

            label.passport_printed = bool(
                row["passport_printed"]
            )

        if "sticker_printed" in row.keys():

            label.sticker_printed = bool(
                row["sticker_printed"]
            )

        # =====================================================
        # Комплектующие
        # =====================================================

        label.items = (
            self._load_items(
                serial
            )
        )

        return label

    # ---------------------------------------------------------

    def _load_items(
        self,
        build_serial: str,
    ) -> list[Item]:

        cursor = self.cursor()

        cursor.execute(
            """
            SELECT

                id,
                category,
                name,
                quantity,
                serial_number

            FROM build_items

            WHERE build_serial = ?

            ORDER BY id
            """,
            (build_serial,),
        )

        rows = cursor.fetchall()

        items = []

        for row in rows:

            category = (
                self._category_from_value(
                    row["category"]
                )
            )

            if category is None:

                category = (
                    Category.OTHER
                )

            item = Item(
                category=category,
                name=row["name"] or "",
                quantity=row["quantity"] or 1,
                serial_number=(
                    row["serial_number"]
                    or ""
                ),
                db_id=row["id"],
            )

            items.append(
                item
            )

        return items

    # ---------------------------------------------------------

    @staticmethod
    def _category_from_value(
        value: str,
    ) -> Category | None:

        for category in Category:

            if (
                str(category.value)
                == str(value)
            ):

                return category

        return None

    # ---------------------------------------------------------

    def _mark_printed(
        self,
        serial: str,
        field: str,
    ) -> bool:
        """
        Отмечает документ как напечатанный.

        Одновременно сохраняет:
        - флаг печати;
        - дату печати;
        - пользователя.

        Это нужно для истории и аудита.
        """

        cursor = self.cursor()

        allowed_fields = {
            "spec_printed",
            "passport_printed",
            "sticker_printed",
        }

        if field not in allowed_fields:

            raise ValueError(
                "Недопустимое поле состояния печати."
            )

        # Например:
        #
        # spec_printed
        # ->
        # spec_printed_at
        # spec_printed_by
        #
        # passport_printed
        # ->
        # passport_printed_at
        # passport_printed_by

        printed_at = (
            f"{field}_at"
        )

        printed_by = (
            f"{field}_by"
        )

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            f"""
            UPDATE builds

            SET
                {field}=1,
                {printed_at}=?,
                {printed_by}=?

            WHERE serial=?

            """,
            (
                now,
                self.user_service.current_user,
                serial,
            ),
        )

        self.commit()

        return cursor.rowcount > 0

    # ---------------------------------------------------------

    def print_specifications(
        self,
        serials: list[str],
        first_position: int = 1,
    ) -> bool:

        labels = []

        for serial in serials:

            label = self.load_label(
                serial
            )

            if label:

                labels.append(
                    label
                )

        if not labels:

            return False

        self.printer.print_to_printer(
            labels,
            first_position,
        )

        for serial in serials:

            self._mark_printed(
                serial,
                "spec_printed",
            )

        return True

    # ---------------------------------------------------------

    def print_passport(
        self,
        serial: str,
    ) -> bool:

        label = self.load_label(
            serial
        )

        if label is None:

            return False

        self.printer.print_passport(
            label
        )

        return self._mark_printed(
            serial,
            "passport_printed",
        )

    # ---------------------------------------------------------

    def print_sticker(
        self,
        serial: str,
    ) -> bool:

        label = self.load_label(
            serial
        )

        if label is None:

            return False

        self.printer.print_sticker(
            label
        )

        return self._mark_printed(
            serial,
            "sticker_printed",
        )

    # ---------------------------------------------------------

    def close(self):

        self.printer.close()
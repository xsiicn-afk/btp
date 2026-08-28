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
        label,
    ):

        model_name = (
            label.model_name
            or label.title
            or label.internal_name
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = self.db.cursor()

        try:

            cursor.execute(
                """
                INSERT OR REPLACE INTO builds(
                    serial,
                    article_code,
                    internal_name,
                    title,
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

                    model_name,
                    product_code,
                    operating_system,
                    warranty_months
                )
                VALUES(
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    label.serial,
                    label.article_code,
                    model_name,
                    model_name,

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

                    label.created_by,
                    label.version,
                    int(label.spec_printed),
                    int(label.passport_printed),
                    int(label.sticker_printed),

                    model_name,
                    label.product_code,
                    label.operating_system,
                    label.warranty_months,
                ),
            )

            cursor.execute(
                """
                DELETE FROM build_items
                WHERE build_serial = ?
                """,
                (label.serial,),
            )

            self._save_items(cursor, label)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
    # ---------------------------------------------------------

    def _save_items(self, cursor, label: LabelModel):

        if not label.items:
            return

        for item in label.items:

            category = item.category

            if hasattr(category, "value"):
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
                VALUES(?, ?, ?, ?, ?)
                """,
                (
                    label.serial,
                    str(category),
                    item.name,
                    item.quantity,
                    item.serial_number or "",
                ),
            )

            item.db_id = cursor.lastrowid

    # ---------------------------------------------------------

    def update_item_serial(
        self,
        item_id: int,
        serial_number: str,
    ) -> bool:

        if item_id is None:
            return False

        serial_number = (serial_number or "").strip()

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

            return cursor.rowcount > 0

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------

    def delete_build(
        self,
        serial: str,
    ) -> bool:
        """
        Полностью удаляет изделие вместе со всеми
        комплектующими и серийными номерами.
        """

        cursor = self.cursor()

        try:

            cursor.execute(
                "DELETE FROM build_items WHERE build_serial = ?",
                (serial,),
            )

            cursor.execute(
                "DELETE FROM builds WHERE serial = ?",
                (serial,),
            )

            deleted = cursor.rowcount > 0

            self.commit()

            return deleted

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

        label.serial = row["serial"] or ""

        if "article_code" in row.keys():
            label.article_code = row["article_code"] or 0
        if "product_code" in row.keys():
            label.product_code = row["product_code"] or ""

        if "model_name" in row.keys() and row["model_name"]:
            label.model_name = row["model_name"]
        elif "title" in row.keys() and row["title"]:
            label.model_name = row["title"]
        else:
            label.model_name = ""

        if "operating_system" in row.keys():
            label.operating_system = row["operating_system"] or ""

        if "warranty_months" in row.keys():
            value = row["warranty_months"]
            label.warranty_months = value if value is not None else 36
        else:
            label.warranty_months = 36

        label.cpu = row["cpu"] or ""
        label.motherboard = row["motherboard"] or ""
        label.cooler = row["cooler"] or ""
        label.ram = row["ram"] or ""
        label.storage = row["storage"] or ""
        label.gpu = row["gpu"] or ""
        label.case = row["pc_case"] or ""
        label.psu = row["psu"] or ""
        label.date = row["build_date"] or ""

        if "created_by" in row.keys():
            label.created_by = row["created_by"] or ""

        if "version" in row.keys():
            label.version = row["version"] or 1

        if "spec_printed" in row.keys():
            label.spec_printed = bool(row["spec_printed"])

        if "passport_printed" in row.keys():
            label.passport_printed = bool(row["passport_printed"])

        if "sticker_printed" in row.keys():
            label.sticker_printed = bool(row["sticker_printed"])

        label.items = self._load_items(serial)

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

            category = self._category_from_value(row["category"])

            if category is None:
                category = Category.OTHER

            item = Item(
                category=category,
                name=row["name"] or "",
                quantity=row["quantity"] or 1,
                serial_number=row["serial_number"] or "",
                db_id=row["id"],
            )

            items.append(item)

        return items

    # ---------------------------------------------------------

    @staticmethod
    def _category_from_value(value: str) -> Category | None:

        for category in Category:
            if str(category.value) == str(value):
                return category

        return None

    # ---------------------------------------------------------

    def _mark_printed(
        self,
        serial: str,
        field: str,
    ) -> bool:

        cursor = self.cursor()

        allowed_fields = {
            "spec_printed",
            "passport_printed",
            "sticker_printed",
        }

        if field not in allowed_fields:
            raise ValueError("Недопустимое поле состояния печати.")

        printed_at = f"{field}_at"
        printed_by = f"{field}_by"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    def print_specification(
        self,
        serial: str,
    ) -> bool:

        label = self.load_label(serial)

        if label is None:
            return False

        self.printer.print_to_printer(label)

        return self._mark_printed(
            serial,
            "spec_printed",
        )

    # ---------------------------------------------------------

    def print_passport(
        self,
        serial: str,
    ) -> bool:

        label = self.load_label(serial)

        if label is None:
            return False

        self.printer.print_passport(label)

        return self._mark_printed(serial, "passport_printed")

    # ---------------------------------------------------------

    def print_sticker(
        self,
        serial: str,
    ) -> bool:

        label = self.load_label(serial)

        if label is None:
            return False

        self.printer.print_sticker(label)

        return self._mark_printed(serial, "sticker_printed")

    # ---------------------------------------------------------

    def close(self):
        self.printer.close()
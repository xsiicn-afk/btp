from datetime import datetime

from database.database import Database
from models.label_model import LabelModel
from services.user_service import UserService


class BuildHistoryService:

    def __init__(self):

        self.db = Database()

        self.user_service = UserService()

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

        cursor = self.cursor()

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO builds(

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
                deleted

            )

            VALUES(

                ?, ?, ?, ?,

                ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?, ?, ?,

                ?, ?, ?, ?

            )
            """,
            (
                label.serial,
                label.article_code,
                label.internal_name,
                label.title,

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

        self.commit()
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

        label.serial = row["serial"]
        label.article_code = row["article_code"]
        label.internal_name = row["internal_name"]
        label.title = row["title"]

        label.cpu = row["cpu"]
        label.motherboard = row["motherboard"]
        label.cooler = row["cooler"]
        label.ram = row["ram"]
        label.storage = row["storage"]
        label.gpu = row["gpu"]
        label.case = row["pc_case"]
        label.psu = row["psu"]

        label.date = row["build_date"]

        if "created_by" in row.keys():

            label.created_by = row["created_by"]

        if "version" in row.keys():

            label.version = row["version"]

        return label
    # ---------------------------------------------------------

    def _mark_printed(
        self,
        serial: str,
        field: str,
    ) -> bool:

        cursor = self.cursor()

        cursor.execute(
            f"""
            UPDATE builds

            SET {field}=1

            WHERE serial=?
            """,
            (serial,),
        )

        self.commit()

        return cursor.rowcount > 0

    # ---------------------------------------------------------

    def print_specification(
        self,
        serial: str,
    ) -> bool:

        #
        # Здесь позже будет вызов сервиса печати спецификации
        #

        return self._mark_printed(
            serial,
            "spec_printed",
        )

    # ---------------------------------------------------------

    def print_passport(
        self,
        serial: str,
    ) -> bool:

        #
        # Здесь позже будет вызов сервиса печати паспорта
        #

        return self._mark_printed(
            serial,
            "passport_printed",
        )

    # ---------------------------------------------------------

    def print_sticker(
        self,
        serial: str,
    ) -> bool:

        #
        # Здесь позже будет вызов сервиса печати наклейки
        #

        return self._mark_printed(
            serial,
            "sticker_printed",
        )

from datetime import datetime

from database.database import Database
from models.label_model import LabelModel


class BuildHistoryService:

    def __init__(self):

        self.db = Database()

    # ---------------------------------------------------------

    def save(
        self,
        label: LabelModel,
    ):

        cursor = self.db.cursor()

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
                created_at

            )

            VALUES(

                ?, ?, ?, ?,

                ?, ?, ?, ?, ?, ?, ?, ?,

                ?, ?

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
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            ),
        )

        self.db.commit()

    # ---------------------------------------------------------

    def all(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *

            FROM builds

            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    # ---------------------------------------------------------

    def load_label(
        self,
        serial: str,
    ) -> LabelModel | None:

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *

            FROM builds

            WHERE serial=?
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

        return label
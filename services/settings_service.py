from database.database import Database


class SettingsService:

    def __init__(self):

        self.db = Database()

        self._create_defaults()

    # ---------------------------------------------------------

    def _create_defaults(self):

        defaults = {

            "template_path": "resources/templates/Спецификация.xlsx",

            "pdf_folder": "pdf",

            "printer": "",

        }

        cursor = self.db.cursor()

        for key, value in defaults.items():

            cursor.execute(
                """
                INSERT OR IGNORE INTO settings
                (key, value)

                VALUES (?, ?)
                """,
                (key, value),
            )

        self.db.commit()

    # ---------------------------------------------------------

    def get(self, key):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT value
            FROM settings
            WHERE key=?
            """,
            (key,),
        )

        row = cursor.fetchone()

        if row:

            return row["value"]

        return ""

    # ---------------------------------------------------------

    def set(self, key, value):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE settings

            SET value=?

            WHERE key=?
            """,
            (
                value,
                key,
            ),
        )

        self.db.commit()
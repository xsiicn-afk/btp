from database.database import Database


class SettingsService:

    def __init__(self):

        self.db = Database()

        self._create_defaults()

    # ---------------------------------------------------------

    def _create_defaults(self):

        defaults = {

            # -------------------------------------------------
            # Шаблоны документов
            # -------------------------------------------------

            "template_path":
                "resources/templates/spec_v2.xlsx",

            "passport_template_path":
                "resources/templates/pass.xlsx",

            "sticker_template_path":
                "resources/templates/sticker.btw",

            # -------------------------------------------------
            # Принтеры
            # -------------------------------------------------

            "spec_printer":
                "",

            "passport_printer":
                "",

            "sticker_printer":
                "",

        }

        cursor = self.db.cursor()

        for key, value in defaults.items():

            cursor.execute(
                """
                INSERT OR IGNORE INTO settings(

                    key,
                    value

                )

                VALUES(

                    ?, ?

                )
                """,
                (
                    key,
                    value,
                ),
            )

        # ---------------------------------------------
        # Перенос старой настройки printer
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT value

            FROM settings

            WHERE key='printer'
            """
        )

        row = cursor.fetchone()

        if row:

            old_printer = (
                row["value"]
                or ""
            )

            if old_printer:

                for key in (
                    "spec_printer",
                    "passport_printer",
                    "sticker_printer",
                ):

                    cursor.execute(
                        """
                        UPDATE settings

                        SET value=?

                        WHERE key=?
                        """,
                        (
                            old_printer,
                            key,
                        ),
                    )

                cursor.execute(
                    """
                    DELETE FROM settings

                    WHERE key='printer'
                    """
                )

        cursor.execute(
            """
            DELETE FROM settings

            WHERE key='pdf_folder'
            """
        )

        self.db.commit()

    # ---------------------------------------------------------

    def get(
        self,
        key,
    ):

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

            return (
                row["value"]
                or ""
            )

        return ""
    # ---------------------------------------------------------

    def set(
        self,
        key,
        value,
    ):

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

    # ---------------------------------------------------------

    def get_spec_printer(self):

        return self.get(
            "spec_printer"
        )

    # ---------------------------------------------------------

    def get_passport_printer(self):

        return self.get(
            "passport_printer"
        )

    # ---------------------------------------------------------

    def get_sticker_printer(self):

        return self.get(
            "sticker_printer"
        )

    # ---------------------------------------------------------

    def set_spec_printer(
        self,
        printer,
    ):

        self.set(
            "spec_printer",
            printer,
        )

    # ---------------------------------------------------------

    def set_passport_printer(
        self,
        printer,
    ):

        self.set(
            "passport_printer",
            printer,
        )

    # ---------------------------------------------------------

    def set_sticker_printer(
        self,
        printer,
    ):

        self.set(
            "sticker_printer",
            printer,
        )
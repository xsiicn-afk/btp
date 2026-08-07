from pathlib import Path
import sqlite3


class Database:

    def __init__(self):

        data_dir = Path("data")

        data_dir.mkdir(
            exist_ok=True
        )

        self.db_file = (
            data_dir / "bytop.db"
        )

        self.connection = sqlite3.connect(
            self.db_file
        )

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    # ---------------------------------------------------------

    def create_tables(self):

        cursor = self.connection.cursor()

        # =====================================================
        # Пользователи
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT UNIQUE NOT NULL,

                active INTEGER DEFAULT 1

            )
            """
        )

        cursor.executemany(
            """
            INSERT OR IGNORE INTO users(name)

            VALUES(?)
            """,
            [
                ("Иванов",),
                ("Петров",),
                ("Сидоров",),
            ],
        )

        # =====================================================
        # Справочник моделей
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS models(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                article_code INTEGER UNIQUE NOT NULL,

                signature TEXT UNIQUE NOT NULL,

                internal_name TEXT NOT NULL,

                model_name TEXT NOT NULL,

                created_at TEXT NOT NULL

            )
            """
        )

        # =====================================================
        # История сборок
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS builds(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                serial TEXT UNIQUE NOT NULL,

                article_code INTEGER NOT NULL,

                internal_name TEXT NOT NULL,

                title TEXT NOT NULL,

                cpu TEXT,

                motherboard TEXT,

                cooler TEXT,

                ram TEXT,

                storage TEXT,

                gpu TEXT,

                pc_case TEXT,

                psu TEXT,

                build_date TEXT NOT NULL,

                created_at TEXT NOT NULL

            )
            """
        )

        # -----------------------------------------------------
        # Обновление существующей таблицы builds
        # -----------------------------------------------------

        self._upgrade_builds(
            cursor
        )

        # =====================================================
        # Комплектующие конкретных выпущенных компьютеров
        #
        # Здесь будут храниться:
        #
        # - категория;
        # - полное название из исходной спецификации;
        # - количество;
        # - серийный номер комплектующего.
        #
        # Один компьютер может иметь сколько угодно строк.
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS build_items(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                build_serial TEXT NOT NULL,

                category TEXT NOT NULL,

                name TEXT NOT NULL,

                quantity INTEGER NOT NULL DEFAULT 1,

                serial_number TEXT DEFAULT '',

                FOREIGN KEY(build_serial)
                REFERENCES builds(serial)

            )
            """
        )

        # -----------------------------------------------------
        # Индекс для быстрого поиска комплектующих
        # по серийному номеру компьютера.
        # -----------------------------------------------------

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_build_items_build_serial

            ON build_items(build_serial)
            """
        )

        # =====================================================
        # Настройки
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings(

                key TEXT PRIMARY KEY,

                value TEXT

            )
            """
        )

        self.connection.commit()

    # ---------------------------------------------------------

    def _upgrade_builds(
        self,
        cursor,
    ):

        """
        Обновляет существующую таблицу builds.

        Старую базу удалять не требуется.
        Недостающие столбцы добавляются
        автоматически при запуске программы.
        """

        cursor.execute(
            "PRAGMA table_info(builds)"
        )

        existing = {
            row["name"]
            for row in cursor.fetchall()
        }

        columns = {

            # -------------------------------------------------
            # Кто создал / изменил изделие
            # -------------------------------------------------

            "created_by":
                "TEXT",

            "modified_at":
                "TEXT",

            "modified_by":
                "TEXT",

            "version":
                "INTEGER DEFAULT 1",

            # -------------------------------------------------
            # Состояние печати
            # -------------------------------------------------

            "spec_printed":
                "INTEGER DEFAULT 0",

            "passport_printed":
                "INTEGER DEFAULT 0",

            "sticker_printed":
                "INTEGER DEFAULT 0",
            # -------------------------------------------------
            # Дата и пользователь печати
            # -------------------------------------------------

            "spec_printed_at":
                "TEXT",

            "spec_printed_by":
                "TEXT",

            "passport_printed_at":
                "TEXT",

            "passport_printed_by":
                "TEXT",

            "sticker_printed_at":
                "TEXT",

            "sticker_printed_by":
                "TEXT",
            # -------------------------------------------------
            # Мягкое удаление
            # -------------------------------------------------

            "deleted":
                "INTEGER DEFAULT 0",

            # -------------------------------------------------
            # Новые поля
            # -------------------------------------------------

            "model_name":
                "TEXT DEFAULT ''",

            "operating_system":
                "TEXT DEFAULT ''",

            "warranty_months":
                "INTEGER DEFAULT 36",
        }

        for name, sql_type in columns.items():

            if name in existing:

                continue

            cursor.execute(
                f"""
                ALTER TABLE builds
                ADD COLUMN {name} {sql_type}
                """
            )

        # =====================================================
        # Совместимость со старой схемой печати
        #
        # В некоторых старых версиях проекта были поля:
        #
        # spec_printed_at
        # passport_printed_at
        # sticker_printed_at
        #
        # Если они существуют, переносим их состояние
        # в новые булевы поля.
        # =====================================================

        cursor.execute(
            "PRAGMA table_info(builds)"
        )

        existing = {
            row["name"]
            for row in cursor.fetchall()
        }

        if (
            "spec_printed" in existing
            and "spec_printed_at" in existing
        ):

            cursor.execute(
                """
                UPDATE builds

                SET spec_printed =
                    CASE
                        WHEN spec_printed_at IS NULL
                        THEN 0
                        ELSE 1
                    END
                """
            )

        if (
            "passport_printed" in existing
            and "passport_printed_at" in existing
        ):

            cursor.execute(
                """
                UPDATE builds

                SET passport_printed =
                    CASE
                        WHEN passport_printed_at IS NULL
                        THEN 0
                        ELSE 1
                    END
                """
            )

        if (
            "sticker_printed" in existing
            and "sticker_printed_at" in existing
        ):

            cursor.execute(
                """
                UPDATE builds

                SET sticker_printed =
                    CASE
                        WHEN sticker_printed_at IS NULL
                        THEN 0
                        ELSE 1
                    END
                """
            )

        self.connection.commit()

    # ---------------------------------------------------------

    def cursor(self):

        return self.connection.cursor()

    # ---------------------------------------------------------

    def commit(self):

        self.connection.commit()

    # ---------------------------------------------------------

    def rollback(self):

        self.connection.rollback()

    # ---------------------------------------------------------

    def execute(
        self,
        sql,
        params=(),
    ):

        cursor = self.cursor()

        cursor.execute(
            sql,
            params,
        )

        self.commit()

        return cursor

    # ---------------------------------------------------------

    def close(self):

        self.connection.close()
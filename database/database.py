from pathlib import Path
import sqlite3


class Database:

    def __init__(self):

        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        self.db_file = data_dir / "bytop.db"

        self.connection = sqlite3.connect(self.db_file)

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
            ]
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
        # Выпущенные компьютеры
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

        self._upgrade_builds(cursor)

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

    def _upgrade_builds(self, cursor):

        cursor.execute("PRAGMA table_info(builds)")

        existing = {
            row["name"]
            for row in cursor.fetchall()
        }

        columns = {

            "created_by":
                "TEXT",

            "modified_at":
                "TEXT",

            "modified_by":
                "TEXT",

            "version":
                "INTEGER DEFAULT 1",

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

            "deleted":
                "INTEGER DEFAULT 0"

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

    # ---------------------------------------------------------

    def cursor(self):

        return self.connection.cursor()

    # ---------------------------------------------------------

    def commit(self):

        self.connection.commit()

    # ---------------------------------------------------------

    def close(self):

        self.connection.close()
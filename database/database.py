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

    def cursor(self):

        return self.connection.cursor()

    # ---------------------------------------------------------

    def commit(self):

        self.connection.commit()

    # ---------------------------------------------------------

    def close(self):

        self.connection.close()
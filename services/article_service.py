from datetime import datetime

from database.database import Database


class ArticleService:

    def __init__(self):

        self.db = Database()

    # ---------------------------------------------------------

    def get_or_create(
        self,
        signature: str,
        model_name: str,
        internal_name: str,
    ) -> int:
        """
        Возвращает код модели.

        Если модель уже существует —
        возвращает существующий код.

        Иначе создаёт новую запись.
        """

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT article_code
            FROM models
            WHERE signature=?
            """,
            (signature,),
        )

        row = cursor.fetchone()

        if row:

            return row["article_code"]

        # -------------------------------------------------
        # Генерация нового артикула
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT MAX(article_code) AS max_code
            FROM models
            """
        )

        row = cursor.fetchone()

        if row["max_code"] is None:

            article_code = 101000

        else:

            article_code = row["max_code"] + 1

        # -------------------------------------------------
        # Новая модель
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO models(

                article_code,
                signature,
                internal_name,
                model_name,
                created_at

            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                article_code,
                signature,
                internal_name,
                model_name,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            ),
        )

        self.db.commit()

        return article_code
from database.database import Database


class UserService:
    """
    Глобальный сервис текущего пользователя.

    Один экземпляр на всё приложение.
    """

    _instance = None
    _current_user = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.database = Database()

        return cls._instance

    # ---------------------------------------------------------

    def users(self):

        cursor = self.database.cursor()

        cursor.execute(
            """
            SELECT
                name
            FROM
                users
            WHERE
                active = 1
            ORDER BY
                name
            """
        )

        return [
            row["name"]
            for row in cursor.fetchall()
        ]

    # ---------------------------------------------------------

    @property
    def current_user(self):

        return self._current_user

    # ---------------------------------------------------------

    def set_current_user(self, name):

        self._current_user = name

    # ---------------------------------------------------------

    def add_user(self, name):

        cursor = self.database.cursor()

        cursor.execute(
            """
            INSERT INTO users(name)
            VALUES(?)
            """,
            (name,)
        )

        self.database.commit()

    # ---------------------------------------------------------

    def deactivate_user(self, name):

        cursor = self.database.cursor()

        cursor.execute(
            """
            UPDATE users
            SET active = 0
            WHERE name = ?
            """,
            (name,)
        )

        self.database.commit()
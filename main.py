import sys

from PySide6.QtWidgets import QApplication

from services.user_service import UserService
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    #
    # Выбор пользователя
    #

    login = LoginDialog()

    if not login.exec():

        sys.exit(0)

    user_service = UserService()

    user_service.set_current_user(
        login.selected_user()
    )

    #
    # Главное окно
    #

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()
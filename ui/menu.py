from PySide6.QtGui import QAction


def create_menu(window):
    menu_bar = window.menuBar()

    file_menu = menu_bar.addMenu("Файл")
    settings_menu = menu_bar.addMenu("Настройки")
    help_menu = menu_bar.addMenu("Справка")

    exit_action = QAction("Выход", window)
    exit_action.triggered.connect(window.close)

    file_menu.addAction(exit_action)
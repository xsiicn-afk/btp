from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)

from services.user_service import UserService


class LoginDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.user_service = UserService()

        self.setWindowTitle("ByTop Production Suite")

        self.setMinimumWidth(320)

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Выберите пользователя:")
        )

        self.users = QComboBox()

        self.users.addItems(
            self.user_service.users()
        )

        layout.addWidget(self.users)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok
            | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(buttons)

    # ---------------------------------------------------------

    def selected_user(self):

        return self.users.currentText()
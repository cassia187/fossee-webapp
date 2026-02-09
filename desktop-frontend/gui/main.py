import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow

from login import Ui_LoginDialog
from signup import Ui_SignupDialog
from dashboard import Ui_MainWindow


class LoginWindow(QDialog, Ui_LoginDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.loginButton.clicked.connect(self.handle_login)
        self.signupLabel.linkActivated.connect(self.open_signup)  # FIXED

    def handle_login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        self.open_dashboard(username)

        # TODO: add authentication and login

    def open_signup(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()

    def open_dashboard(self, username):
        self.dashboard_window = DashboardWindow(username)  # FIXED
        self.dashboard_window.show()
        self.close()


class SignupWindow(QDialog, Ui_SignupDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.signupButton.clicked.connect(self.handle_signup)
        self.loginLabel.linkActivated.connect(self.go_to_login)  # FIXED

    def handle_signup(self):
        username = self.usernameInput.text()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        # TODO: Add registration logic

        self.go_to_login()

    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class DashboardWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.username = username

        self.welcomeLabel.setText(f"Welcome, {self.username}")

        self.logoutButton.clicked.connect(self.handle_logout)

    def handle_logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()

    sys.exit(app.exec_())
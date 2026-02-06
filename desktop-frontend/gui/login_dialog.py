from PyQt5.QtWidgets import QDialog, QLabel,QMessageBox, QVBoxLayout, QLineEdit, QPushButton

class LoginDialog(QDialog):
    # uses api.client for authentication
    def __init__(self, api_client): 
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Login to Visualizer")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        

        self.setLayout(layout)
        

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()

        if self.api_client.login(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
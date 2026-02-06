from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QFileDialog, QLabel
from api.client import APIClient
from gui.login_dialog import LoginDialog
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import QRect, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.setWindowTitle("Visualizer")
        self.setGeometry(100, 100, 800, 600)

        login_dialog = LoginDialog(self.api_client)
        if login_dialog.exec_() == QDialog.Accepted:
            self.show()

        self.init_ui()
        self.load_datasets()

    def init_ui(self):
        center = QWidget()
        self.setCentralWidget(center)
        layout = QVBoxLayout(center)
        layout.setSpacing(20)  # Gap between widgets
        layout.setContentsMargins(30, 30, 30, 30) # Padding around window

        # Label
        title_label = QLabel("My Datasets")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Profile info
        profile_label = QLabel("Profile")
        profile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(profile_label)

        self.username_label = QLabel("Username: Loading...")
        self.email_label = QLabel("Email: Loading...")
        layout.addWidget(self.username_label)
        layout.addWidget(self.email_label)
        
        self.show_profile()

        # Button (Left aligned)
        self.upload_btn = QPushButton("Upload Dataset (csv)")
        self.upload_btn.setFixedSize(200, 40)
        # Align center horizontally
        layout.addWidget(self.upload_btn, alignment=Qt.AlignLeft)

        # List of datasets
        self.datasets_list = QListWidget()
        self.datasets_list.itemClicked.connect(self.show_details)
        
        layout.addWidget(self.datasets_list)
        
        center.setLayout(layout)

    def upload_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "CSV Files (*.csv)")
        if path:
            result = self.api_client.upload_dataset(path)
            if result:
                QMessageBox.information(self, "Success", "Dataset uploaded successfully")
                self.load_datasets()
            else:
                QMessageBox.warning(self, "Error", "Failed to upload dataset")
    
    def load_datasets(self):
        # clear old list when clicked
        self.datasets_list.clear()
        # json response here
        datasets = self.api_client.get_datasets()
        for dataset in datasets:
            self.datasets_list.addItem(f"{dataset['filename']} | ({dataset['total_count']} items)")
        
    def show_details(self, item):
        QMessageBox.information(self, 'Dataset', f'selected: {item.text()}')
    
    def show_profile(self):
        profile = self.api_client.get_profile()
        if profile:
            self.username_label.setText(f"Username: {profile['user']['username']}")
            self.email_label.setText(f"Email: {profile['user']['email']}")
        else:
            self.username_label.setText("Username: Error")
            self.email_label.setText("Email: Error")
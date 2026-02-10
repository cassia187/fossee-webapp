import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, 
                             QFileDialog, QListWidgetItem)
from PyQt5.QtCore import Qt

from .login import Ui_LoginDialog
from .signup import Ui_SignupDialog
from .dashboard import Ui_MainWindow
from api.api_client import APIClient


class LoginWindow(QDialog, Ui_LoginDialog):
    def __init__(self, api_client):
        super().__init__()
        self.setupUi(self)
        self.api_client = api_client

        # Connect signals
        self.loginButton.clicked.connect(self.handle_login)
        self.signupLabel.linkActivated.connect(self.open_signup)
        
        # Allow pressing Enter to login
        self.passwordInput.returnPressed.connect(self.handle_login)

    def handle_login(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text()

        # Validate inputs
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return

        # Attempt login via API
        result = self.api_client.login(username, password)
        
        if result['success']:
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_dashboard(username)
        else:
            QMessageBox.critical(self, "Login Failed", result['message'])

    def open_signup(self):
        self.signup_window = SignupWindow(self.api_client)
        self.signup_window.show()
        self.close()

    def open_dashboard(self, username):
        self.dashboard_window = DashboardWindow(username, self.api_client)
        self.dashboard_window.show()
        self.close()


class SignupWindow(QDialog, Ui_SignupDialog):
    def __init__(self, api_client):
        super().__init__()
        self.setupUi(self)
        self.api_client = api_client

        # Connect signals
        self.signupButton.clicked.connect(self.handle_signup)
        self.loginLabel.linkActivated.connect(self.go_to_login)
        
        # Allow pressing Enter to signup
        self.passwordInput.returnPressed.connect(self.handle_signup)

    def handle_signup(self):
        username = self.usernameInput.text().strip()
        email = self.emailInput.text().strip()
        password = self.passwordInput.text()

        # Validate inputs
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        if '@' not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid email address")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long")
            return

        # Attempt registration via API
        result = self.api_client.register(username, email, password)
        
        if result['success']:
            QMessageBox.information(self, "Success", 
                                  "Registration successful! You can now login.")
            self.go_to_login()
        else:
            QMessageBox.critical(self, "Registration Failed", result['message'])

    def go_to_login(self):
        self.login_window = LoginWindow(self.api_client)
        self.login_window.show()
        self.close()


class DashboardWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username, api_client):
        super().__init__()
        self.setupUi(self)
        self.username = username
        self.api_client = api_client
        self.current_dataset_id = None

        # Update welcome label
        self.label.setText(f"Welcome, {self.username}")

        # Connect signals
        self.logout_btn.clicked.connect(self.handle_logout)
        self.uploadbtn.clicked.connect(self.handle_upload)
        self.deletebtn.clicked.connect(self.handle_delete)
        
        # Connect list widget selection
        self.dataset_list.itemClicked.connect(self.on_dataset_selected)
        
        # Load datasets
        self.load_datasets()

    def load_datasets(self):
        """Load and display all datasets"""
        self.dataset_list.clear()
        datasets = self.api_client.get_datasets()
        
        if datasets:
            for dataset in datasets:
                # Display dataset filename in the list
                item = QListWidgetItem(dataset['filename'])
                # Store dataset ID in item data
                item.setData(Qt.UserRole, dataset['id'])
                self.dataset_list.addItem(item)
        else:
            # Show message if no datasets
            item = QListWidgetItem("No datasets uploaded yet")
            item.setFlags(Qt.NoItemFlags)  # Make it non-selectable
            self.dataset_list.addItem(item)

    def on_dataset_selected(self, item):
        """Handle dataset selection from list"""
        dataset_id = item.data(Qt.UserRole)
        
        if dataset_id:
            self.current_dataset_id = dataset_id
            # TODO: Load and visualize dataset data
            # You can call self.visualize_dataset(dataset_id) here
            print(f"Selected dataset ID: {dataset_id}")

    def handle_upload(self):
        """Handle CSV file upload"""
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            # Upload via API
            result = self.api_client.upload_dataset(file_path)
            
            if result['success']:
                QMessageBox.information(self, "Success", result['message'])
                # Reload datasets list
                self.load_datasets()
            else:
                QMessageBox.critical(self, "Upload Failed", result['message'])

    def handle_delete(self):
        """Handle dataset deletion"""
        # Get selected item
        current_item = self.dataset_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a dataset to delete")
            return
        
        dataset_id = current_item.data(Qt.UserRole)
        
        if not dataset_id:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{current_item.text()}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete via API
            result = self.api_client.delete_dataset(dataset_id)
            
            if result['success']:
                QMessageBox.information(self, "Success", result['message'])
                # Reload datasets list
                self.load_datasets()
            else:
                QMessageBox.critical(self, "Delete Failed", result['message'])

    def visualize_dataset(self, dataset_id):
        """
        TODO: Visualize dataset using matplotlib
        
        Steps:
        1. Get dataset details: self.api_client.get_dataset_details(dataset_id)
        2. Get type distribution: self.api_client.get_type_distribution(dataset_id)
        3. Create matplotlib plots and display in the QWidget (matplotlibWidget)
        
        Example:
        details = self.api_client.get_dataset_details(dataset_id)
        distribution = self.api_client.get_type_distribution(dataset_id)
        
        # Create matplotlib figure and plot
        # Embed in self.matplotlibWidget (or whatever you named it)
        """
        pass

    def handle_logout(self):
        """Handle logout"""
        # Logout via API
        result = self.api_client.logout()
        
        if result['success']:
            self.login_window = LoginWindow(self.api_client)
            self.login_window.show()
            self.close()
        else:
            # Still logout locally even if API call fails
            self.api_client.token = None
            self.login_window = LoginWindow(self.api_client)
            self.login_window.show()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create API client instance
    api_client = APIClient(base_url="http://localhost:8000/api")
    
    # Check if server is running
    if not api_client.health_check():
        QMessageBox.warning(
            None,
            "Server Not Running",
            "Cannot connect to the API server.\n\n"
            "Please make sure the Django server is running:\n"
            "python manage.py runserver"
        )
    
    # Start with login window
    login = LoginWindow(api_client)
    login.show()
    
    sys.exit(app.exec_())

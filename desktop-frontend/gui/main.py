import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QVBoxLayout, QListWidgetItem, QFileDialog
from .login import Ui_LoginDialog
from .signup import Ui_SignupDialog
from .dashboard import Ui_MainWindow
from .data_visualizer import DataVisualizer
from .matplotlib_widget import MatplotlibWidget
from api.api_client import APIClient


class LoginWindow(QDialog, Ui_LoginDialog):
    def __init__(self, api_client):
        super().__init__()
        self.setupUi(self)
        self.api_client = api_client

        # Button connections to trigger next stage of UI
        self.loginButton.clicked.connect(self.handle_login)
        self.signupLabel.linkActivated.connect(self.open_signup)

        # Allow Enter key to login
        self.passwordInput.returnPressed.connect(self.handle_login)

    def handle_login(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter your username and password.")
            return

        # send to /api/login
        result = self.api_client.login(username, password)

        if result['success']:
            QMessageBox.information(self, "Success", "Login successful.")
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

        self.signupButton.clicked.connect(self.handle_signup)
        self.loginLabel.linkActivated.connect(self.go_to_login)

        self.passwordInput.returnPressed.connect(self.handle_signup)

    def handle_signup(self):
        username = self.usernameInput.text().strip()
        email = self.emailInput.text().strip()
        password = self.passwordInput.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill all the fields")
            return

        if '@' not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid email address.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters.")
            return

        # Send to /api/register (NOT signup!)
        result = self.api_client.register(username, email, password)

        if result['success']:
            QMessageBox.information(self, "Success", "Signup successful. You may now login.")
            self.go_to_login()
        else:
            QMessageBox.critical(self, "Registration failed", result['message'])

    def go_to_login(self):
        self.login_window = LoginWindow(self.api_client)
        self.login_window.show()
        self.close()


class DashboardWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username, api_client):
        super().__init__()
        self.setupUi(self)
        self.resize(1400, 1000)
        self.setMinimumSize(900, 600)
        self.username = username
        self.api_client = api_client
        self.current_dataset_id = None

        # Setup matplotlib widget first
        self.setup_matplotlib_widget()
        self.visualizer = DataVisualizer(self.mpl_widget.get_figure())

        # Update welcome label (widget name is 'label' in your dashboard.py)
        self.label.setText(f"Welcome, {self.username}")

        # Connect buttons (use actual widget names from dashboard.py)
        self.logout_btn.clicked.connect(self.handle_logout)
        self.uploadbtn.clicked.connect(self.handle_upload)
        self.deletebtn.clicked.connect(self.handle_delete)

        # Connect list widget (actual name is 'dataset_list')
        self.dataset_list.itemClicked.connect(self.on_dataset_clicked)

        # Load datasets and show welcome
        self.load_datasets()
        self.show_welcome_message()

    def setup_matplotlib_widget(self):
        """Setup matplotlib widget in the right panel"""
        self.mpl_widget = MatplotlibWidget(self)

        try:
            # Get the placeholder widget
            placeholder = self.plotWidget

            # Get its parent widget
            parent = placeholder.parentWidget()

            if parent:
                # Get parent's layout
                parent_layout = parent.layout()

                if parent_layout:
                    # Replace placeholder with matplotlib widget
                    parent_layout.replaceWidget(placeholder, self.mpl_widget)
                    placeholder.deleteLater()
                else:
                    # Create new layout if none exists
                    layout = QVBoxLayout(parent)
                    layout.addWidget(self.mpl_widget)
            else:
                QMessageBox.warning(
                    self,
                    "Widget Error",
                    "Could not find parent for plotWidget"
                )
        except AttributeError as e:
            QMessageBox.warning(
                self,
                "Widget Not found",
                f"Could not find 'plotWidget' in the UI: {str(e)}\n\n"
                "Please add a QWidget named 'plotWidget' to your dashboard.ui "
                "for the visualization area"
            )

    def show_welcome_message(self):
        """Show welcome message on the plot area"""
        self.mpl_widget.clear()
        fig = self.mpl_widget.get_figure()
        ax = fig.add_subplot(111)
        ax.axis('off')

        welcome_text = f"""
        Welcome to Equipment Data Analyzer

        {self.username}

        ────────────────────────────────

        To get started:

        1. Upload a CSV dataset using the Upload button
        2. Select a dataset from the list on the left
        3. View visualizations and statistics here

        Your datasets will be displayed with:
        • Equipment type distribution
        • Average parameters by type
        • Flowrate vs Pressure analysis
        • Temperature distribution
        """

        ax.text(0.5, 0.5, welcome_text, fontsize=12,
                ha="center", va="center",
                bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5))

        self.mpl_widget.draw()

    def load_datasets(self):
        """Load and display all datasets"""
        self.dataset_list.clear()
        datasets = self.api_client.get_datasets()

        if datasets:
            for dataset in datasets:
                item = QListWidgetItem(dataset["filename"])
                item.setData(Qt.UserRole, dataset['id'])
                self.dataset_list.addItem(item)
        else:
            # No datasets found
            item = QListWidgetItem("No datasets uploaded yet")
            item.setFlags(Qt.NoItemFlags)
            self.dataset_list.addItem(item)

    def on_dataset_clicked(self, item):
        """Handle dataset selection"""
        dataset_id = item.data(Qt.UserRole)

        if dataset_id:
            self.current_dataset_id = dataset_id
            self.visualize_dataset(dataset_id)

    def handle_upload(self):
        """Handle CSV file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All files (*)"
        )

        if file_path:
            QMessageBox.information(
                self,
                "Uploading",
                "Uploading Dataset... This may take a moment"
            )

            result = self.api_client.upload_dataset(file_path)

            if result['success']:
                QMessageBox.information(self, "Success", result['message'])
                # Reload datasets
                self.load_datasets()

                # Auto-select newly uploaded dataset
                if result.get('dataset'):
                    new_dataset_id = result['dataset']['id']
                    for i in range(self.dataset_list.count()):
                        item = self.dataset_list.item(i)
                        if item.data(Qt.UserRole) == new_dataset_id:
                            self.dataset_list.setCurrentItem(item)
                            self.visualize_dataset(new_dataset_id)
                            break
            else:
                QMessageBox.critical(self, "Upload Failed", result["message"])

    def handle_delete(self):
        """Handle dataset deletion"""
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
            result = self.api_client.delete_dataset(dataset_id)

            if result['success']:
                QMessageBox.information(self, "Success", result['message'])

                # Clear visualization if this was the selected dataset
                if self.current_dataset_id == dataset_id:
                    self.current_dataset_id = None
                    self.show_welcome_message()

                # Reload datasets
                self.load_datasets()
            else:
                QMessageBox.critical(self, "Delete Failed", result["message"])

    def visualize_dataset(self, dataset_id):
        """Visualize the selected dataset"""
        # Get dataset details
        details = self.api_client.get_dataset_details(dataset_id)

        if not details:
            QMessageBox.warning(
                self,
                "Error",
                "Could not load dataset details."
            )
            return

        # Get type distribution
        distribution = self.api_client.get_type_distribution(dataset_id)

        if not distribution:
            QMessageBox.warning(
                self,
                "Error",
                "Could not load distribution data."
            )
            return

        # Create visualizations
        try:
            self.visualizer.create_dashboard(details, distribution)
            self.mpl_widget.draw()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Visualization Error",
                f"Error creating visualizations: {str(e)}"
            )
            print(f"Visualization Error: {e}")
            import traceback
            traceback.print_exc()

    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Logout via API
            result = self.api_client.logout()

            # Clear token and return to login
            self.api_client.token = None
            self.login_window = LoginWindow(self.api_client)
            self.login_window.show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create API client
    api_client = APIClient(base_url="http://localhost:8000/api")

    # Check if server is running
    if not api_client.health_check():
        reply = QMessageBox.warning(
            None,
            "Server Not Running",
            "Cannot connect to the API server.\n\n"
            "Please make sure the Django server is running:\n"
            "python manage.py runserver\n\n"
            "Continue anyway?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            sys.exit(0)

    # Start with login window
    login = LoginWindow(api_client)
    login.show()

    sys.exit(app.exec_())
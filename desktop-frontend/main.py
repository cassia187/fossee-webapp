from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QMainWindow
import sys
from gui.main_win import MainWindow

def main():
    app = QApplication(sys.argv)
    # window = QMainWindow()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
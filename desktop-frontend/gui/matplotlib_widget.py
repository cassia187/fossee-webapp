from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QAction, QFileDialog


class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(Canvas, self).__init__(self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.canvas = Canvas(self, width=8, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # remove certain actions from toolbar
        for action in self.toolbar.actions():
            text = action.text().lower()
            if any(k in text for k in ["save", "customize", "subplot", "edit"]):
                self.toolbar.removeAction(action)
        save_pdf_action = QAction("Save PDF", self)
        save_pdf_action.triggered.connect(self.save_pdf)
        self.toolbar.addAction(save_pdf_action)

        # Vertical Qt layout on the right side on dashboard
        # -----------Toolbar-----------
        # -----------Canvas------------
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def get_figure(self):
        return self.canvas.fig

    def clear(self):
        self.canvas.fig.clear()
        self.canvas.draw()

    def draw(self):
        return self.canvas.draw()

    def save_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if file_path:
            if not file_path.endswith(".pdf"):
                file_path += ".pdf"

            self.canvas.fig.savefig(file_path, format="pdf")

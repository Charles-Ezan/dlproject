from PySide2.QtWidgets import QMainWindow,  QApplication


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Test app name")
        self.setCentralWidget(widget)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Status Bar
        self.status = self.statusBar()
        # TO DO: gérer le status de l'app (si la prédiction est en cours de calcul ou si elle est calculée
        if widget.isPredicted:
            self.status.showMessage("Data loaded and plotted")
        else:
            self.status.showMessage("Loading data")

        # Window dimensions
        geometry = QApplication.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

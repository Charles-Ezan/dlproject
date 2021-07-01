from PySide2.QtWidgets import QMainWindow,  QApplication


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Cryptocurrencies forecasting")
        self.setCentralWidget(widget)

        # Window dimensions
        geometry = QApplication.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

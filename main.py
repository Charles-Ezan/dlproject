import sys
from PySide2.QtWidgets import QApplication
from main_window import MainWindow
from main_widget import Widget

if __name__ == "__main__":

    # Qt Application
    app = QApplication(sys.argv)

    widget = Widget()
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())
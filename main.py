import sys
import pandas as pd

from PySide2.QtWidgets import QApplication
from main_window import MainWindow
from main_widget import Widget

def read_data(file):
    # Read the CSV content
    return pd.read_csv(file)

if __name__ == "__main__":

    # Qt Application
    app = QApplication(sys.argv)

    widget = Widget()
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())
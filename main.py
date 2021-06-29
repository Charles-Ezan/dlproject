import sys
import pandas as pd

from PySide2.QtWidgets import QApplication
from main_window import MainWindow
from main_widget import Widget

def read_data(file):
    # Read the CSV content
    return pd.read_csv(file)

if __name__ == "__main__":

    data_btc = read_data("XRP_USD_2020-06-23_2021-06-22-CoinDesk.csv")
    data_xrp = read_data("ADA_USD_2020-06-23_2021-06-22-CoinDesk.csv")

    # Qt Application
    app = QApplication(sys.argv)

    widget = Widget(data_btc, data_xrp)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())
import sys
import pandas as pd

from PySide2.QtWidgets import QApplication
from main_window import MainWindow
from main_widget import Widget
from training import testModel, getClosePrice, preprocessing, reshape, splitData


def read_data(file):
    # Read the CSV content
    return pd.read_csv(file)


if __name__ == "__main__":
    data_btc = read_data("bitcoin_small_dataset.csv")

    dataset, granularity = getClosePrice(1392577232, 1422577232)
    data, target = preprocessing(dataset, 40, 1)
    X_train, X_test, y_train, y_test = splitData(data, target, shuffle=False)
    X_train, X_test = reshape(X_train, X_test)
    model_name = "savedmodel"

    data_xrp = testModel(X_test, y_test, model_name)

    # Qt Application
    app = QApplication(sys.argv)

    widget = Widget(data_btc, data_xrp)
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())

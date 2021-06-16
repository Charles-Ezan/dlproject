# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
# from PyQt5.QtChart import QChart, QChartView

from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Crypto forecasting")
        self.setGeometry(300,300,1000,700)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    # Titre de la crypto
    cryptoTitle = QLabel(window)
    cryptoTitle.setText("Bitcoin")
    cryptoTitle.move(100,100)
    # Valeur finale
    finalValue = QLabel(window)
    finalValue.setText("xxxxx$")
    finalValue.move(750,100)
    # Delta de prédiction
    error = QLabel(window)
    error.setText("x,xx%")
    error.move(800,100)
    # Bouton run
    b1 = QPushButton(window)
    b1.setText("Run")
    b1.move(400,600)
    # Bouton 1 semaine
    buttonWeek = QPushButton(window)
    buttonWeek.setText("1 week")
    buttonWeek.move(670,500)
    # Bouton 1 mois
    buttonMonth = QPushButton(window)
    buttonMonth.setText("1 month")
    buttonMonth.move(760,500)
    # Graphique


    window.show()
    sys.exit(app.exec())

from PySide2.QtCore import QDateTime, Qt
from PySide2.QtGui import QPainter
import pandas as pd
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QComboBox, QBoxLayout
from PySide2.QtCharts import QtCharts


# from table_model import CustomTableModel


class Widget(QWidget):
    def __init__(self, data1, data2):
        QWidget.__init__(self)
        self.isPredicted = True

        # Getting the Model
        self.crypto = data1
        self.prediction = data2

        # Creating QChart
        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.init_chart(data1, data2)

        # Creating QChartView
        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        size.setHorizontalStretch(1)
        train_button = QPushButton('Train')
        test_button = QPushButton('Test')
        cryptocurrencie_title = QLabel('<h2>Bitcoin</h2>')
        cryptocurrencie_title.setSizePolicy(size)
        final_label = QLabel('Valeur finale: ' + 'xxxx$')
        error_label = QLabel('Erreur moyenne: ' + 'xx,x%')
        rmse_label = QLabel('RMSE: ' + 'xxx')

        left_box = QVBoxLayout()
        buttons = QHBoxLayout()

        buttons.addWidget(train_button)
        left_box.addSpacing(10)
        buttons.addWidget(test_button)
        left_box.addWidget(cryptocurrencie_title)
        left_box.addWidget(final_label)
        left_box.addWidget(error_label)
        left_box.addWidget(rmse_label)
        left_box.addSpacing(5)
        left_box.addLayout(buttons)
        left_box.addStretch(1)
        train_button.clicked.connect(self.test_click)
        self.main_layout.addLayout(left_box)

        # Right Layout
        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)
        self.chart_view.setFixedSize(1000, 700)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def test_click(self):
        self.init_chart(self.crypto, self.prediction)

    def init_chart(self, data_crypto, data_prediction):
        # On s'assure que le graphique ne contient aucune donnée
        self.chart.removeAllSeries()

        self.serie1 = QtCharts.QLineSeries()
        self.serie1.setName('Court réel')

        # Filling QLineSeries
        for index, row in data.iterrows():
            t = row['date']
            date_fmt = "yyyy-MM-dd"

            x = QDateTime().fromString(t, date_fmt).toSecsSinceEpoch()
            self.serie1.append(x, float(row['Closing Price (USD)']))

        self.serie2 = QtCharts.QLineSeries()
        self.serie2.setName('Prédiction')

        # Filling QLineSeries
        for index, row in data_prediction.iterrows():
            t2 = str(row['Date'])
            date_fmt = "yyyy-MM-dd"
            x2 = QDateTime().fromString(t2, date_fmt).toSecsSinceEpoch()
            self.serie2.append(x2, float(row['Closing Price (USD)']))
        self.chart.addSeries(self.serie1)
        self.chart.addSeries(self.serie2)

        # Setting X-axis
        self.axis_x = QtCharts.QDateTimeAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setFormat('dd.MM')
        self.axis_x.setTitleText('Date')
        self.chart.setAxisX(self.axis_x)
        self.serie1.attachAxis(self.axis_x)
        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat('%.2f')
        self.axis_y.setTitleText('Price')
        self.chart.setAxisY(self.axis_y)
        # Pour l'instant l'axe y s'oriente autour des valeurs de la prédiction
        #       donc le cours réel peut être ammené à sortir du graph
        # TO DO: get le min et max des deux courbes pour fixer l'axe
        # self.axis_y.setRange(1.0,1.5)
        # self.serie1.attachAxis(self.axis_y)
        self.serie2.attachAxis(self.axis_y)
        # self.chart.setTitle(str(data.loc[0,'Currency']))

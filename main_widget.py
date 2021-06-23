from PySide2.QtCore import QDateTime, Qt
from PySide2.QtGui import QPainter
import pandas as pd
from PySide2.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QPushButton,
                               QSizePolicy)
from PySide2.QtCharts import QtCharts

# from table_model import CustomTableModel


class Widget(QWidget):
    def __init__(self, data1, data2):
        QWidget.__init__(self)
        self.isPredicted = True
        # Getting the Model
        # self.model = CustomTableModel(data)
        self.bitcoin = data1
        self.ripple = data2

        # Creating QChart
        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        # self.add_series('Magnitude (Column 1)', [0, 3])
        self.init_chart(data1, data2)

        # Creating QChartView
        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        size.setHorizontalStretch(2)
        run = QPushButton('Run')
        # self.run.setSizePolicy(size)
        self.main_layout.addWidget(run)
        run.clicked.connect(self.test_click)
        # Right Layout
        size.setHorizontalStretch(3)
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)


    def test_click(self):
        self.init_chart(self.bitcoin, self.ripple)

    def init_chart(self, data, data_bis):
        # On s'assure que le graphique ne contient aucune donnée
        self.chart.removeAllSeries()

        self.serie1 = QtCharts.QLineSeries()
        self.serie1.setName('Court réel')

        # Filling QLineSeries
        for index, row in data.iterrows():
            t= row['Date']
            date_fmt = "yyyy-MM-dd"

            x = QDateTime().fromString(t, date_fmt).toSecsSinceEpoch()
            self.serie1.append(x, float(row['Closing Price (USD)']))

        self.serie2 = QtCharts.QLineSeries()
        self.serie2.setName('Prédiction')

        # Filling QLineSeries
        for index, row in data_bis.iterrows():
            t2= str(row['Date'])
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
        self.serie1.attachAxis(self.axis_y)
        self.serie2.attachAxis(self.axis_y)

        self.chart.setTitle(str(data.loc[0,'Currency']))
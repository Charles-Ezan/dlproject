from PySide2.QtGui import QPainter
import pandas as pd
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox
from PySide2.QtCharts import QtCharts
import training

class Widget(QWidget):
    def __init__(self, ):
        QWidget.__init__(self)
        self.isPredicted = True

        # Getting the datas
        btc_prices, btc_gran, btc_time = training.getClosePrice(1392577232, 1622577232)
        eth_prices, eth_gran, eth_time = training.getClosePrice(1392577232, 1622577232, coin_id='ethereum')
        self.btc = pd.DataFrame({'date': btc_time, 'price': btc_prices})
        self.eth = pd.DataFrame({'date': eth_time, 'price': eth_prices})

        # Creating QChart
        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.init_chart(self.btc, 'Bitcoin') #The default crypto is the bitcoin

        # Creating QChartView
        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # QWidget Layout
        self.main_layout = QHBoxLayout()

        # Left layout
        left_box = QVBoxLayout()
        title_box = QHBoxLayout()
        model_box = QHBoxLayout()
        button_box = QHBoxLayout()
            # Train Button
        train_button = QPushButton('Train')
        train_button.clicked.connect(self.train_click)
            # Test Button
        test_button = QPushButton('Test')
        test_button.clicked.connect(self.test_click)
            # Crypto choice
        crypto_text = QLabel('Cryptomonnaie :')
        cryptocurrencie_title = QComboBox()
        cryptocurrencie_title.addItems(['Bitcoin', 'Ethereum'])
        cryptocurrencie_title.currentIndexChanged.connect(self.crypto_change)
            # Labels
        error_label = QLabel('Erreur moyenne: '+ 'xx,x%')
        rmse_label = QLabel('RMSE: '+'xxx')
            # Model choice
        model_text = QLabel('Modèle :')
        models_button = QComboBox()
        models_button.addItems(['<none>', 'Saved model'])
        models_button.currentIndexChanged.connect(self.model_change)

        title_box.addWidget(crypto_text)
        title_box.addWidget(cryptocurrencie_title)
        left_box.addLayout(title_box)
        model_box.addWidget(model_text)
        model_box.addWidget(models_button)
        left_box.addLayout(model_box)
        left_box.addSpacing(15)
        left_box.addWidget(error_label)
        left_box.addWidget(rmse_label)
        left_box.addSpacing(10)
        button_box.addWidget(train_button)
        button_box.addWidget(test_button)
        left_box.addLayout(button_box)
        left_box.addStretch(1)
        self.main_layout.addLayout(left_box)

        # Right Layout
        self.chart_view.setFixedSize(1000, 700)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def crypto_change(self, i):
        if i == 1:
            data = self.eth
            title = 'Ethereum'
        else:
            data = self.btc
            title = 'Bitcoin'
        self.init_chart(data, title)

    def model_change(self, i):
        if i == 0:
            return

    def init_chart(self, data, title):
        # On s'assure que le graphique ne contient aucune donnée
        self.chart.removeAllSeries()

        self.serie1 = QtCharts.QLineSeries()
        self.serie1.setName('Court réel')

        # Filling QLineSeries
        for index, row in data.iterrows():
            self.serie1.append(row['date'], row['price'])

        # Filling QChart
        self.chart.addSeries(self.serie1)
        # self.chart.createDefaultAxes()

        # Setting X-axis
        self.axis_x = QtCharts.QDateTimeAxis()
        self.axis_x.setFormat('MM/yyyy')
        self.axis_x.setTitleText('Date')
        self.chart.setAxisX(self.axis_x)
        self.serie1.attachAxis(self.axis_x)

        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setLabelFormat('%.2f $')
        self.axis_y.setTitleText('Prix (USD)')
        self.chart.setAxisY(self.axis_y)
        self.serie1.attachAxis(self.axis_y)

        # Setting the title
        self.chart.setTitle(title)


    def train_click(self):
        self.add_prediction(self.eth)

    def test_click(self):
        self.add_prediction(self.eth)

    def add_prediction(self, data):
        # We remove any other prediction on the chart to avoid superposition
        series = self.chart.series()
        if len(series) > 1:
            series.pop(0)
            for s in series:
                self.chart.removeSeries(s)

        self.serie1 = QtCharts.QLineSeries()
        self.serie1.setName('Prédiction')

        # Filling QLineSeries
        for index, row in data.iterrows():
            self.serie1.append(row['date'], row['price'])

        # Filling QChart
        self.chart.addSeries(self.serie1)
        self.chart.createDefaultAxes()

        # Setting X-axis
        self.axis_x = QtCharts.QDateTimeAxis()
        self.axis_x.setFormat('MM/yyyy')
        self.axis_x.setTitleText('Date')
        self.chart.setAxisX(self.axis_x)
        self.serie1.attachAxis(self.axis_x)

        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setLabelFormat('%.2f $')
        self.axis_y.setTitleText('Prix (USD)')
        self.chart.setAxisY(self.axis_y)
        self.serie1.attachAxis(self.axis_y)
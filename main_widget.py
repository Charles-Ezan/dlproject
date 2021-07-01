from PySide2.QtGui import QPainter
import pandas as pd
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QRadioButton
from PySide2.QtCharts import QtCharts
import training

class Widget(QWidget):
    def __init__(self, ):
        QWidget.__init__(self)
        self.aWeekIsChecked = True
        self.isBtc = True
        self.RMSE = 0.0
        self.error = 0.0

        # Getting the datas
        btc_prices, btc_gran, btc_time = training.getClosePrice(1392577232, 1622577232)
        eth_prices, eth_gran, eth_time = training.getClosePrice(1392577232, 1622577232, coin_id='ethereum')
        self.btc = pd.DataFrame({'date': btc_time, 'price': btc_prices})
        self.eth = pd.DataFrame({'date': eth_time, 'price': eth_prices})
        # a week = 1621972432
        #          1392595200000
        #          1392577232
        #          1622160000000
        # a month =1619942032
        # Creating QChart
        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.init_chart() #The default crypto is the bitcoin

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
        prediction_box = QHBoxLayout()
            # Train Button
        train_button = QPushButton('Train')
        train_button.clicked.connect(self.train_click)
            # Test Button
        test_button = QPushButton('Test')
        test_button.clicked.connect(self.test_click)
            # Crypto choice
        crypto_text = QLabel('Cryptomonnaie :')
        crypto_title = QComboBox()
        crypto_title.addItems(['Bitcoin', 'Ethereum'])
        crypto_title.currentIndexChanged.connect(self.crypto_change)
            # Labels
        self.error_label = QLabel('Erreur moyenne: --%')
        self.rmse_label = QLabel('RMSE: '+str(self.RMSE))
            # Model choice
        model_text = QLabel('Modèle :')
        models_button = QComboBox()
        models_button.addItems(['<none>', 'Saved model'])
        models_button.currentIndexChanged.connect(self.model_change)
            # Prediction duration
        prediction_title = QLabel('Prédiction sur :')
        week = QRadioButton("Une semaine")
        week.setChecked(True)
        week.toggled.connect(lambda: self.prediction_size(week))

        month = QRadioButton("Un mois")
        month.toggled.connect(lambda: self.prediction_size(month))
        prediction_box.addWidget(prediction_title)
        prediction_box.addWidget(week)
        prediction_box.addWidget(month)

        # Adding crypto to layout
        title_box.addWidget(crypto_text)
        title_box.addWidget(crypto_title)
        left_box.addLayout(title_box)
        # Adding models to layout
        model_box.addWidget(model_text)
        model_box.addWidget(models_button)
        left_box.addLayout(model_box)
        left_box.addLayout(prediction_box)
        left_box.addSpacing(15)
        # Adding error labels
        left_box.addWidget(self.error_label)
        left_box.addWidget(self.rmse_label)
        left_box.addSpacing(10)
        # Adding train/test buttons
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
            self.isBtc = False
        else:
            self.isBtc = True
        self.init_chart()

    def model_change(self, i):
        if i == 0:
            return

    def init_chart(self):
        # On s'assure que le graphique ne contient aucune donnée
        self.chart.removeAllSeries()

        self.serie1 = QtCharts.QLineSeries()
        self.serie1.setName('Court réel')
        data = self.btc
        title = 'Bitcoin'
        if self.isBtc == False:
            data = self.eth
            title = 'Ethereum'
        limit = 1621972432000
        if self.aWeekIsChecked == False:
            limit = 1619942032000

        # Filling QLineSeries
        for index, row in data.iterrows():
            if row['date']>limit:
                self.serie1.append(row['date'], row['price'])

        # Filling QChart
        self.chart.addSeries(self.serie1)

        # Setting X-axis
        self.axis_x = QtCharts.QDateTimeAxis()
        self.axis_x.setFormat('dd/MM')
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
        self.chart.scroll(50.0, 10.0)

    def prediction_size(self,b):
        if b.text() == 'Une semaine':
            if b.isChecked():
                self.aWeekIsChecked = True
            else:
                self.aWeekIsChecked = False
        else:
            if b.isChecked():
                self.aWeekIsChecked = False
            else:
                self.aWeekIsChecked = True
        self.init_chart()


    def add_prediction(self, data):
        # We remove any other prediction on the chart to avoid superposition
        series = self.chart.series()
        if len(series) > 1:
            series.pop(0)
            for s in series:
                self.chart.removeSeries(s)

        self.calculate_error(data)

        self.serie1 = QtCharts.QLineSeries()
        self.serie1.setName('Prédiction')

        limit = 1621972432000
        if self.aWeekIsChecked == False:
            limit = 1619942032000

        # Filling QLineSeries
        for index, row in data.iterrows():
            if row['date'] > limit:
                self.serie1.append(row['date'], row['price'])

        # Filling QChart
        self.chart.addSeries(self.serie1)
        self.chart.createDefaultAxes()

        # Setting X-axis
        self.axis_x = QtCharts.QDateTimeAxis()
        self.axis_x.setFormat('dd/MM')
        self.axis_x.setTitleText('Date')
        self.chart.setAxisX(self.axis_x)
        self.serie1.attachAxis(self.axis_x)

        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setLabelFormat('%.2f $')
        self.axis_y.setTitleText('Prix (USD)')
        self.chart.setAxisY(self.axis_y)
        self.serie1.attachAxis(self.axis_y)

    def calculate_error(self, prediction):
        data = self.btc
        if not self.isBtc:
            data = self.eth
        limit = 1621972432000
        if not self.aWeekIsChecked:
            limit = 1619942032000
        datalist = []
        predlist = []
        for index, row in data.iterrows():
            if row['date']>limit:
                datalist.append(row['price'])
        for index, row in prediction.iterrows():
            if row['date']>limit:
                predlist.append(row['price'])

        operation = [abs(a_i - b_i)/a_i for a_i, b_i in zip(datalist, predlist)]
        self.error = round(100*sum(operation)/len(operation), 2)
        self.error_label.setText('Erreur moyenne: '+str(self.error)+'%')
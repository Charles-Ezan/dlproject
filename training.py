import numpy as np
import pandas as pd
import tensorflow
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.model_selection import train_test_split
from keras.models import model_from_json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import math
from sklearn.metrics import mean_squared_error
from pycoingecko import CoinGeckoAPI
import json

physical_devices = tensorflow.config.list_physical_devices('GPU')
tensorflow.config.experimental.set_memory_growth(physical_devices[0], enable=True)

cg = CoinGeckoAPI()


def getClosePrice(from_date, to_date, vs_currency='usd', coin_id='bitcoin'):
    delta_date = to_date - from_date
    if delta_date < 86400:
        # One day
        granularity = "minutes"
    if delta_date < 7776000:
        # 90 days
        granularity = "hours"
    if delta_date >= 7776000:
        # Above 90 days
        granularity = "days"

    price = cg.get_coin_market_chart_range_by_id(coin_id, vs_currency, from_date, to_date)
    close_prices = []
    timestamp = []
    for prices in price["prices"]:
        close_prices.append(prices[1])
        timestamp.append(prices[0])

    return close_prices, granularity, timestamp


# Creating train and test dataset
def preprocessing(dataset, data_size, target_size):
    data = []
    target = []
    for i in range(len(dataset) - (data_size + target_size)):
        data_sample = []
        target_sample = []
        for j in range(data_size):
            data_sample.append(format(dataset[i + j], '.2f'))
        data.append(data_sample)
        for k in range(target_size):
            target_sample.append(format(dataset[i + data_size + k], '.2f'))
        target.append(target_sample)

    data = np.array(data)
    target = np.array(target)
    data = data.astype('float64')
    target = target.astype('float64')
    scaler = MinMaxScaler(feature_range=(0, 1))  # Normalization between 0 and 1
    data = scaler.fit_transform(data)

    return data, target


# Creating train and test dataset
def splitData(data, target, test_size=0.1, shuffle=True):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=test_size, random_state=42,
                                                        shuffle=shuffle)

    return X_train, X_test, y_train, y_test


def reshape(X_train, X_test):
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    return X_train, X_test


def trainModel(X_train, y_train, model_name):
    model_file = model_name
    model = Sequential()
    model.add(LSTM(128, input_shape=(1, 40)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='sgd')
    model.fit(X_train, y_train, epochs=1, batch_size=1, verbose=1)
    saveModel(model, model_file)


def testModel(X_test, y_test, model_file):
    model = loadModel(model_file)
    y_pred = model.predict(X_test)
    testScore = math.sqrt(mean_squared_error(y_test, y_pred))
    print('Test Score: %.2f RMSE' % testScore)
    print("y_test =", y_test, "Predict =", y_pred)
    return y_pred
    # plt.plot(y_test)
    # plt.plot(y_pred)
    # plt.legend(['original value', 'predicted value'], loc='upper right')
    # plt.show()


def saveModel(model, model_file):
    # serialize model to JSON
    model_json = model.to_json()
    with open(model_file, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")


def loadModel(model_file):
    # load json and create model
    json_file = open(model_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    return loaded_model


def addTimestampToPrediction(price_prediction, timestamp, test_size=0.1):
    fullPrediction = []
    timestamp=np.array(timestamp)
    print(type(price_prediction), type(timestamp), price_prediction, timestamp)
    breakpoint()
    pandaPrediction = pd.DataFrame(fullPrediction, ['Date', 'Close_price'])


start_timestamp, finish_timestamp = 1392577232, 1422577232
dataset, granularity, timestamp = getClosePrice(start_timestamp, finish_timestamp)
data, target = preprocessing(dataset, 40, 1)
X_train, X_test, y_train, y_test = splitData(data, target, shuffle=False)
X_train, X_test = reshape(X_train, X_test)
model_name = "savedmodel"
pred = testModel(X_test, y_test, model_name)
addTimestampToPrediction(pred, timestamp)
breakpoint()
trainModel(X_train, y_train, model_name)
testModel(X_test, y_test, model_name)

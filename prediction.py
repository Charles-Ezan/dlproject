import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.model_selection import train_test_split
import math
from sklearn.metrics import mean_squared_error

df = pd.read_csv('bitcoin_small_dataset.csv')


# Creating train and test dataset
def preprocessing(dataset):
    dataset = dataset.drop(dataset.index[0])  # Del first line
    #dataset = dataset.drop(['Currency'], axis=1)  # Del currency column
    dataset = dataset.drop(['date'], axis=1)  # Del date column

    data = dataset.iloc[:, 1:]
    target = dataset.iloc[:, 0]  # Closing price

    data = data.values
    data = data.astype('float64')
    scaler = MinMaxScaler(feature_range=(0, 1))  # Normalization between 0 and 1
    data = scaler.fit_transform(data)
    target = target.values

    return data, target


# Creating train and test dataset
def splitData(data, target, test_size=0.2, shuffle=True):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=test_size, random_state=42,
                                                        shuffle=shuffle)

    return X_train, X_test, y_train, y_test


def reshape(X_train, X_test):
    print(X_train.shape[0])
    breakpoint()
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    return X_train, X_test


def trainModel(X_train, y_train):
    model = Sequential()
    model.add(LSTM(64, input_shape=(1, 4)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='sgd')
    print(X_train, y_train)
    breakpoint()
    model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=1)

    return model


def testModel(model, X_test, y_test):
    y_pred = model.predict(X_test)
    testScore = math.sqrt(mean_squared_error(y_test, y_pred))
    print('Test Score: %.2f RMSE' % testScore)
    print("y_test =", y_test, "Predict =", y_pred)
    plt.plot(y_test)
    plt.plot(y_pred)
    plt.legend(['original value', 'predicted value'], loc='upper right')
    plt.show()


def main():
    data, target = preprocessing(df)
    X_train, X_test, y_train, y_test = splitData(data, target, shuffle=False)
    X_train, X_test = reshape(X_train, X_test)
    model = trainModel(X_train, y_train)
    testModel(model, X_test, y_test)


main()
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

df = pd.read_csv('bitcoin_2011-1-1_2019-1-1.csv', header=None)
df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']

y = df['Close'].values
X = df[['Volume']].values

regr = LinearRegression()

X_fit = np.arange(X.min(), X.max(), 1)[:, np.newaxis]

regr = regr.fit(X, y)
y_lin_fit = regr.predict(X_fit)
linear_r2 = r2_score(y, regr.predict(X))

plt.scatter(X, y, label='training points', color='lightgray')

plt.plot(X_fit, y_lin_fit,
         label='linear (d=1), $R^2=%.2f$' % linear_r2,
         color='blue',
         lw=2,
         linestyle=':')

plt.ylabel('% Clode')
plt.xlabel('Date')
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()

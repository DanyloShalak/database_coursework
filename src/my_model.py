import yfinance as yf
import math
from sklearn.preprocessing import MinMaxScaler
import numpy
from keras.models import Sequential
from keras.layers import LSTM, Dense


def get_predicted_price(history):
    #отримання дата фрейму з цінами
    data = history.filter(['price'])
    #отримання масиву значень
    price_dataset = data.values
    #отриання кількості записів для тренування
    train_data_length = math.ceil(len(price_dataset) * 0.8)

    #skale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(price_dataset)

    #preparing train data
    train_data = scaled_data[0 : train_data_length, :]
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60: i, 0])
        y_train.append(train_data[i, 0])

    #converting to numpy arrays
    x_train = numpy.array(x_train)
    y_train = numpy.array(y_train)

    x_train = numpy.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=1, epochs=1)


    needed_data = history.filter(['price'])
    last_60 = needed_data[-60:].values
    last_60_scaled = scaler.transform(last_60)
    X_test = []
    X_test.append(last_60_scaled)
    X_test = numpy.array(X_test)
    X_test = numpy.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_price = model.predict(X_test)
    predicted_price = scaler.inverse_transform(predicted_price)

    return predicted_price[0][0]








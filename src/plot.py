import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('fivethirtyeight')


def plot_price_history(price_data, p_name):
    plt.figure(figsize=(16, 8))
    plt.title(f'Price History of {p_name}')
    plt.plot(price_data['price'])
    plt.xlabel('Date')
    plt.ylabel('Price(USD)')
    plt.show()


def save_price_history(price_data, save_file_path, p_name):
    plt.figure(figsize=(16, 8))
    plt.title(f'Price History of {p_name}')
    plt.plot(price_data['price'])
    plt.xlabel('Date')
    plt.ylabel('Price(USD)')
    plt.savefig(save_file_path)


def plot_index_test():
    no_ind = pd.read_csv('./testing/testing_data/without_b-tree_index2.csv')
    no_ind = no_ind[['record_count', 'time']]
    no_ind =  no_ind.set_index('record_count')

    ind = pd.read_csv('./testing/testing_data/with_b-tree_index.csv')
    ind = ind[['record_count', 'time']]
    ind =  ind.set_index('record_count')

    plt.figure(figsize=(16, 8))
    plt.plot(no_ind, color='r', label='without index')
    plt.plot(ind, color='b', label='with index')#'with index'
    plt.xlabel('Records count')
    plt.ylabel('Time(microseconds)')
    plt.legend()
    plt.show()
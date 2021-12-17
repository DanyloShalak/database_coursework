import pandas as pd
pd.options.mode.chained_assignment = None
import yfinance as yf
from repository import Repository
from io import StringIO


def get_list_of_symbols(count : int):
    data = pd.read_csv('left.csv')
    symbols_count = len(data)
    if symbols_count == 0:
        raise Exception('No symbols left')
    if symbols_count < count:
        count = symbols_count
    lefted_symbols = data.tail(len(data) - count)
    lefted_symbols.to_csv('left.csv')
    data = data.head(count)
    list_symbols = data['Symbol'].tolist()
    return list_symbols


def generate_prices(product_count : int, repository : Repository):
    symbols = get_list_of_symbols(product_count)
    column_names = ['Date', 'Open', 'ProductId', 'ShopId']
    gen_dataFrame = pd.DataFrame(columns=column_names)

    for symbol in symbols:
        product_id = repository.get_product_id(symbol)
        shop_id = repository.get_shop_id(symbol)
        ticker = yf.Ticker(symbol)
        ticker_history = ticker.history(period='2000d')
        ticker_history.reset_index(inplace=True)
        insertData = ticker_history[['Date', 'Open']]
        insertData['ProductId'] = product_id
        insertData['ShopId'] = shop_id
        gen_dataFrame = gen_dataFrame.append(insertData)
    
    return gen_dataFrame
        



def generate_products(count : int, repository : Repository):
    data = generate_prices(count, repository)
    repository.insert_prices(data)


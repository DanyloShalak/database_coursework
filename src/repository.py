import pandas as pd
from pandas.core.frame import DataFrame
import psycopg2 as ps
from io import StringIO
from psycopg2.extras import RealDictCursor

class Repository:
    def __init__(self):
        self.__master_connection = ps.connect(dbname="cw_database", user="postgres",
                                       password="danylo", host="172.22.0.3")
        self.__master_connection.autocommit = True
        self.__slave_connection = ps.connect(dbname="cw_database", user="postgres",
                                       password="danylo", host="172.22.0.2")

    def get_product_id(self, name):
        cursor = self.__master_connection.cursor()
        cursor.execute("""select get_product_id(%s)""", (name, ))
        id = cursor.fetchone()[0]
        cursor.close()
        return id
    
    def get_shop_id(self, name):
        cursor = self.__master_connection.cursor()
        cursor.execute("""select get_shop_id(%s)""", (name, ))
        id = cursor.fetchone()[0]
        cursor.close()
        return id

    def insert_prices(self, data_frame : DataFrame):
        data_frame = data_frame.set_index('Date')
        buffer = StringIO()
        data_frame.to_csv(buffer, index_label='id', header=False)
        buffer.seek(0)

        cursor = self.__master_connection.cursor()
        try:
            cursor.copy_from(buffer, 'prices', sep=",")
        except (Exception, ps.DatabaseError) as error:
            print("Error: %s" % error)
            self.__connection.rollback()
        cursor.close()

    def get_product_price_history(self, product_name):
        product_id = self.get_product_id(product_name)
        cursor = self.__slave_connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""select prices.price_date, prices.price
                     from prices where product_id = %s""", (product_id, ))
        price_history = cursor.fetchall()
        cursor.close()
        price_history  = pd.DataFrame(price_history)
        print(price_history)
        price_history = price_history.sort_values('price_date')
        price_history = price_history.set_index('price_date')
        return price_history

    
    def insert_product_price_record(self, record):
        cursor = self.__master_connection.cursor()
        record = list(record)
        product_id = self.get_product_id(record[2])
        record[2] = product_id
        shop_id = self.get_shop_id(record[3])
        record[3] = shop_id 
        cursor.execute("""insert into prices(price_date, price, product_id, shop_id)
                        values(%s, %s, %s, %s)""", tuple(record))
        cursor.close()

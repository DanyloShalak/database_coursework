from matplotlib.pyplot import show
from repository import Repository
from plot import plot_price_history, save_price_history
from my_model import get_predicted_price
from new_generator import generate_products

class Controller:

    def __init__(self, repo : Repository):
        self.__repository = repo
        self.__command_dict = {}
        self.__command_dict['showPH'] = self.__show_price_history
        self.__command_dict['savePH'] = self.__save_price_history
        self.__command_dict['predictPrice'] = self.__predict_price
        self.__command_dict['generate'] = self.__generate_products
        self.__command_dict['insert'] = self.__insert_price_record


    def __show_price_history(self, product_name):
        price_history = self.__repository.get_product_price_history(product_name)
        print(price_history)
        plot_price_history(price_history, product_name)
    

    def __save_price_history(self, product_name, save_file_path):
        price_history = self.__repository.get_product_price_history(product_name)
        save_price_history(price_history, product_name, save_file_path)

    
    def __predict_price(self, product_name):
        price_history = self.__repository.get_product_price_history(product_name)
        if len(price_history) < 90:
            raise Exception(f'Not enough record about product "{product_name}"')
        predicted_price = get_predicted_price(price_history)
        print(f"Predicted price for {product_name} is --> {predicted_price} USD")


    def __generate_products(self, product_count):
        product_count = int(product_count)
        if product_count < 0:
            raise Exception('Product count can`t be less than 0')
        generate_products(product_count, self.__repository)


    def __insert_price_record(self, record):
        self.__repository.insert_product_price_record(record)


    def perform_command(self, command_line : str):
        command_line = command_line.split(' ')
        command = command_line[0]

        if command in ['showPH', 'generate', 'predictPrice']:
            self.__command_dict[command](command_line[1])
        elif command == 'savePH':
            self.__command_dict[command](command_line[1], command_line[2])
        elif command == 'insert':
            self.__command_dict[command](tuple(command_line[1:]))
        else:
            print(f'Error: unknown command "{command}"')
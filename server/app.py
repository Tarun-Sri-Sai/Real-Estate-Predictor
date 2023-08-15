from pickle import load as pk_load
from json import load as json_load
from model import run_model
from os import path
from pandas import DataFrame


class App:
    def __init__(self):
        cache_dir = path.join('..', 'data', 'cache')
        headers_path = path.join(cache_dir, 'headers.json')
        model_path = path.join(cache_dir, 'model.sav')
        if not any([path.isfile(headers_path), path.isfile(model_path)]):
            run_model()
        else:
            print(f'Reading headers from {headers_path}')
            print(f'Reading model from {model_path}')
        self.headers = json_load(open(headers_path, 'r'))
        self.model = pk_load(open(model_path, 'rb'))
        self.processed_input = {}
        self.price = 0

    def get_columns(self):
        return self.headers['columns']
    
    def get_data_values(self):
        return self.headers['data_values']

    def process_input(self, input):
        input_encodings = {}
        for key, value in input.items():
            if key in self.headers['encoding_variables']:
                value = self.headers['encodings'][key][input[key]]
            else:
                value = float(input[key])
            input_encodings[key] = value
        self.processed_input = input_encodings

    def get_processed(self):
        return self.processed_input

    def predict_price(self, input):
        ordered_input = {}
        for column in self.get_columns():
            ordered_input[column] = input[column]
        self.price = self.model.predict(DataFrame(ordered_input, index=[0]))[0]

    def get_price(self):
        return self.price

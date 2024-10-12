from pickle import load as pk_load
from json import load as json_load
from model import run_model
from os import path
from pandas import DataFrame
from zipfile import ZipFile


class RealEstate:
    def __init__(self):
        if not path.isdir('data') and path.isfile('data.zip'):
            with ZipFile('data.zip', 'r') as f:
                f.extractall()

        cache_dir = path.join('data', 'cache')
        headers_path = path.join(cache_dir, 'headers.json')
        model_path = path.join(cache_dir, 'model.sav')
        if not any([path.isfile(headers_path), path.isfile(model_path)]):
            run_model()
        else:
            print(f'Reading headers from {headers_path}')
            print(f'Reading model from {model_path}')

        self.headers = json_load(open(headers_path, 'r'))
        self.model = pk_load(open(model_path, 'rb'))

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

        return input_encodings

    def predict_price(self, input):
        ordered_input = {}
        for column in self.get_columns():
            ordered_input[column] = input[column]

        return self.model.predict(DataFrame(ordered_input, index=[0]))[0]

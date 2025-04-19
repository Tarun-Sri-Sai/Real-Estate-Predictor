import pickle
import json
from os import path
from pandas import DataFrame as pd_df
from . import model


class RealEstate:
    def __init__(self):
        cache_dir = path.join('data', 'cache')
        headers_path = path.join(cache_dir, 'headers.json')
        model_path = path.join(cache_dir, 'model.sav')
        if not any([path.isfile(headers_path), path.isfile(model_path)]):
            model.run_model()
        else:
            print(f'Reading headers from {headers_path}')
            print(f'Reading model from {model_path}')

        self.headers = json.load(open(headers_path, 'r'))
        self.model = pickle.load(open(model_path, 'rb'))

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

        return self.model.predict(pd_df(ordered_input, index=[0]))[0]

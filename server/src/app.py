from pickle import load as pk_load
from json import load as json_load
from model import main as run_model
from os import path
from pandas import DataFrame as pd_df


class App:
    def __init__(self):
        catalog_path: str = path.join('..', 'catalog', 'catalog.json')
        model_path: str = path.join('..', 'model', 'model.sav')

        if not any([path.isfile(catalog_path), path.isfile(model_path)]):
            run_model()

        self.catalog = json_load(open(catalog_path, 'r'))
        self.model = pk_load(open(model_path, 'rb'))

        self.processed_input: dict = {}
        self.price: float = 0

    def get_columns(self):
        return self.catalog['columns']
    
    def get_data_values(self):
        return self.catalog['data_values']

    def process_input(self, input: dict):
        input_encodings = {}
        for key, value in input.items():
            input_encodings[key] = value
            if key in self.catalog['encoding_variables']:
                value = self.catalog['encodings'][key][input_encodings[key]]
            else:
                value = float(input_encodings[key])

            input_encodings[key] = value

        self.processed_input = input_encodings

    def get_processed(self):
        return self.processed_input

    def predict_price(self, input):
        ordered_input = {}
        for column in self.get_columns():
            ordered_input[column] = input[column]
        
        self.price = self.model.predict(pd_df(ordered_input, index=[0]))[0]

    def get_price(self):
        return self.price

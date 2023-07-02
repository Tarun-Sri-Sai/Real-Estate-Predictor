import pickle as pk
import pandas as pd

import json
import os
import model


class App:
    def __init__(self):
        catalog_path: str = os.path.join('..', 'catalog', 'catalog.json')
        model_path: str = os.path.join('..', 'model', 'model.sav')

        if not any([os.path.isfile(catalog_path), os.path.isfile(model_path)]):
            model.main()

        self.catalog = json.load(open(catalog_path, 'r'))
        self.model = pk.load(open(model_path, 'rb'))

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
        
        self.price = self.model.predict(pd.DataFrame(ordered_input, index=[0]))[0]

    def get_price(self):
        return self.price

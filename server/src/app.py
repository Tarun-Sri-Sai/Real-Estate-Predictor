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

        return input_encodings

    def get_pred(self, input):
        ordered_input = {}
        for column in self.get_columns():
            ordered_input[column] = input[column]
        return self.model.predict(pd.DataFrame(ordered_input, index=[0]))[0]

from app import App

from flask import Flask, request
from flask_cors import CORS

flask_app = Flask(__name__)
CORS(flask_app)
real_app = App()


@flask_app.route('/real_estate_predictor/column_names', methods=['GET'])
def column_names_endpoint():
    column_names = real_app.get_columns()
    return {'column_names': column_names}


@flask_app.route('/real_estate_predictor/data_values', methods=['GET'])
def data_values_endpoint():
    data_values = real_app.get_data_values()
    return {'data_values': data_values}


@flask_app.route('/real_estate_predictor/input', methods=['POST'])
def input_endpoint():
    input_data = request.json
    real_app.process_input(input_data)
    processed_input = real_app.get_processed()
    return {'processed_input': processed_input}


@flask_app.route('/real_estate_predictor/prediction', methods=['POST'])
def prediction_endpoint():
    processed_input = request.json
    real_app.predict_price(processed_input)
    price_in_lacs = real_app.get_price()
    return {'price_in_lacs': price_in_lacs}


if __name__ == '__main__':
    flask_app.run()

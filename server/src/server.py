from flask import Flask, request
from app import App


flask_app = Flask(__name__)
real_app = App()


@flask_app.route('/get_column_names', methods=['GET'])
def get_column_names():
    column_names = real_app.get_columns()
    return {'column_names': column_names}


@flask_app.route('/get_data_values', methods=['GET'])
def get_data_values():
    data_values = real_app.get_data_values()
    return {'data_values': data_values}


@flask_app.route('/process_input', methods=['POST'])
def process_input():
    input_data = request.get_json()
    processed_input = real_app.process_input(input_data)
    return {'processed_input': processed_input}


@flask_app.route('/get_pred', methods=['POST'])
def get_pred():
    input_data = request.get_json()
    price_in_lacs = real_app.get_pred(input_data)
    return {'price_in_lacs': price_in_lacs}


if __name__ == '__main__':
    flask_app.run()

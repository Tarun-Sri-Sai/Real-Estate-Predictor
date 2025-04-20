from flask import Flask, request
from .real_estate import RealEstate
from json import loads


server = Flask(__name__)
real_estate = RealEstate()


@server.route('/api/column_names', methods=['GET'])
def column_names_endpoint():
    column_names = real_estate.get_columns()
    return {'column_names': column_names}


@server.route('/api/data_values', methods=['GET'])
def data_values_endpoint():
    data_values = real_estate.get_data_values()
    return {'data_values': data_values}


@server.route('/api/prediction', methods=['GET'])
def prediction_endpoint():
    processed_input = real_estate.process_input({
        k: loads(v) for k, v in request.args.items()
    })
    price_in_lacs = real_estate.predict_price(processed_input)
    return {'price_in_lacs': price_in_lacs}

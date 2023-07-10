from app import App

import flask as fl
import flask_cors as fc


flask_app = fl.Flask(__name__)
fc.CORS(flask_app)
real_app = App()


@flask_app.route('/real_estate_predictor/column_names', methods=['GET'])
def column_names_endpoint():
    column_names = real_app.get_columns()
    return {'column_names': column_names}


@flask_app.route('/real_estate_predictor/data_values', methods=['GET'])
def data_values_endpoint():
    data_values = real_app.get_data_values()
    return {'data_values': data_values}


@flask_app.route('/real_estate_predictor/input', methods=['PUT', 'GET'])
def input_endpoint():
    method = fl.request.method

    match method:
        case 'PUT':
            input_data = fl.request.get_json()
            real_app.process_input(input_data)
            return fl.jsonify({'message': 'Success'}), 200
        
        case 'GET':
            processed_input = real_app.get_processed()
            return {'processed_input': processed_input}


@flask_app.route('/real_estate_predictor/prediction', methods=['PUT', 'GET'])
def prediction_endpoint():
    method = fl.request.method
    
    match method:
        case 'PUT':
            processed_input = fl.request.get_json()
            real_app.predict_price(processed_input)
            return fl.jsonify({'message': 'Success'}), 200
        
        case 'GET':
            price_in_lacs = real_app.get_price()
            return {'price_in_lacs': price_in_lacs}


if __name__ == '__main__':
    flask_app.run()

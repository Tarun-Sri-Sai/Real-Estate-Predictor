from app import App

import flask as fl
import flask_cors as fc


flask_app = fl.Flask(__name__)
fc.CORS(flask_app)
real_app = App()


@flask_app.route('/real_estate_predictor/get_column_names', methods=['GET'])
def get_column_names_endpoint():
    column_names = real_app.get_columns()
    return {'column_names': column_names}


@flask_app.route('/real_estate_predictor/get_data_values', methods=['GET'])
def get_data_values_endpoint():
    data_values = real_app.get_data_values()
    return {'data_values': data_values}


@flask_app.route('/real_estate_predictor/process_input', methods=['PUT', 'GET'])
def process_input_endpoint():
    method = fl.request.method

    match method:
        case 'PUT':
            input_data = fl.request.get_json()
            real_app.process_input(input_data)
            return fl.jsonify({'message': 'Success'}), 200
        
        case 'GET':
            processed_input = real_app.get_processed()
            return {'processed_input': processed_input}


@flask_app.route('/real_estate_predictor/predict', methods=['PUT', 'GET'])
def predict_endpoint():
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

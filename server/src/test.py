import requests as rq
import random as rn

# To get column names
response = rq.get('http://localhost:5000/get_column_names')
column_names = response.json()['column_names']

# To get data values
response = rq.get('http://localhost:5000/get_data_values')
data_values = response.json()['data_values']

# To process input data
input_data = dict((column_name, rn.choice(data_values[column_name]))
                  for column_name in column_names)
print(input_data)

response = rq.post('http://localhost:5000/process_input', json=input_data)
processed_input = response.json()['processed_input']

# To get price prediction
response = rq.post('http://localhost:5000/get_pred', json=processed_input)
print(response.json())

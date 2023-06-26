import pandas as pd
import pickle as pk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
import json


def get_plot_type(text: str) -> str:
    text = text.strip()
    if 'BHK' in text:
        return text.split('BHK')[1].strip()

    if 'RK' in text:
        return text.split('RK')[1].strip()

    return text.strip()


def get_bhk(text: str) -> str:
    result = text.strip().replace(get_plot_type(text), '')
    if result == '':
        return 0
    
    return int(result.split()[0])


def encode(column, encodings):
    encoded_column = column.map(encodings)
    return encoded_column


def create_encodings(column, price):
    df_temp = pd.DataFrame({'column': column, 'price': price})
    unique_categories = df_temp['column'].unique()
    avg_prices = df_temp.groupby('column')['price'].mean()
    sorted_categories = list(sorted(unique_categories, key=lambda x: avg_prices[x]))
    encodings = {category: index for index, category in enumerate(sorted_categories)}
    return encodings


def price_to_lacs(text: str) -> float:
  text = text.strip()
  if 'L' in text:
    return int(float(text.split()[0]))

  return int(float(text.split()[0]) * 100)


def main():
    # Reading the CSV file
    df = pd.read_csv(os.path.join('data', 'data.csv'))
    
    # Remove unwanted columns and rename
    df = df.drop('Unnamed: 0', axis=1)
    df.insert(0, 'seller_name', df['Seller Name'].apply(lambda x: x.strip()))
    df = df.drop('Seller Name', axis=1)
    df.insert(1, 'seller_type', df['Seller type'].apply(lambda x: x.strip()))
    df = df.drop('Seller type', axis=1)
    df.insert(2, 'bhk', df['BHK'].apply(lambda x: x.strip()))
    df = df.drop('BHK', axis=1)
    df.insert(3, 'location', df['Location'].apply(lambda x: x.strip()))
    df = df.drop('Location', axis=1)
    df.insert(4, 'city', df['City'].apply(lambda x: x.strip()))
    df = df.drop('City', axis=1)
    df.insert(5, 'price_per_sqft', df['price per sqft'].apply(lambda x: x.strip()))
    df = df.drop('price per sqft', axis=1)
    df.insert(6, 'area', df['Area_sqft'])
    df = df.drop('Area_sqft', axis=1)
    df.insert(7, 'construction_status', df['Construction status'].apply(lambda x: x.strip()))
    df = df.drop('Construction status', axis=1)
    df.insert(8, 'price', df['Total Price'].apply(lambda x: x.strip()))
    df = df.drop('Total Price', axis=1)

    # Extracting plot type from BHK
    df.insert(3, 'plot_type', df['bhk'].apply(get_plot_type))
    df.insert(4, 'bhk/rk', df['bhk'].apply(get_bhk))
    df = df.drop(['bhk'], axis=1)


    # Feature encoding
    encodings = {}
    encoding_variables = ['seller_name', 'seller_type', 'plot_type', 'location', 'city', 'construction_status']
    for column in encoding_variables:
      encodings[column] = create_encodings(df[column], df['price'].apply(price_to_lacs))

    # Creating a numeric dataframe
    df_num = pd.DataFrame()
    for column in encoding_variables:
        df_num[column] = encode(df[column], encodings[column])
    df_num.insert(3, 'bhk/rk', df['bhk/rk'])
    df_num.insert(6, 'area', df['area'])

    # Converting prices to lacs
    df_num['price'] = df['price'].apply(price_to_lacs)
    
    # Removing outliers
    value_counts = df_num['price'].value_counts().to_dict()
    df_fil = df_num[df_num['price'].apply(lambda x: value_counts[x] > 10)]


    # Model training
    X = df_fil.iloc[:, 2:-1]
    Y = df_fil.iloc[:, -1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    model = LinearRegression()
    model.fit(X_train, Y_train)

    # Saving the model
    json.dump({'encoding_variables': encoding_variables, 
           'encodings': encodings, 
           'df_dict': df.to_dict(), 
           'columns': X.columns.tolist()}, open('../cache/input_cache.json', 'w'))
    pk.dump(model, open('../models/linear_regression.sav', 'wb'))


if __name__ == "__main__":
    main()

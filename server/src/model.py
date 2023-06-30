from sklearn.linear_model import LinearRegression

import preprocess as pp
import pandas as pd
import pickle as pk

import os
import json


def get_plot_type(text: str) -> str:
    text = text.strip()
    if 'BHK' in text:
        return text.split('BHK')[1].strip()

    if 'RK' in text:
        return text.split('RK')[1].strip()

    return text.strip()


def get_bhk(text: str) -> int:
    result = text.strip().replace(get_plot_type(text), '')
    if result == '':
        return 0

    return int(result.split()[0])


def price_to_lacs(text: str) -> float:
    text = text.strip()
    if 'L' in text:
        return int(float(text.split()[0]))

    return int(float(text.split()[0]) * 100)



def main():
    # Reading the CSV file
    df: pd.DataFrame = pd.read_csv(os.path.join('..', 'data', 'data.csv'))

    # Preprocessing the dataframe columns
    df = pp.rename(df, df.columns)
    df = pp.strip(df, pp.string_cols(df))

    # Extracting plot type from BHK
    df.insert(4, 'plot_type', df['bhk'].apply(get_plot_type))
    df.insert(5, 'bhk/rk', df['bhk'].apply(get_bhk))

    # Removing unwanted columns
    df = pp.remove(df, ['unnamed_0', 'bhk'])    

    # Adding title case
    df = pp.title(df, ['plot_type', 'construction_status', 'location'])

    # Concatenating city into location
    df['location'] = df['location'] + ', ' + df['city']

    # Converting prices to lacs
    df['total_price'] = df['total_price'].apply(price_to_lacs)

    # Feature encoding
    encodings = {}
    encoding_variables = [
        'seller_name', 'seller_type', 'plot_type',
        'location', 'city', 'construction_status'
    ]
    for column in encoding_variables:
        encodings[column] = pp.create_encodings(
            df[column], df['total_price'])

    # Creating a numeric dataframe
    df_num = pd.DataFrame()
    for column in encoding_variables:
        df_num[column] = pp.encode(df[column], encodings[column])

    df_num.insert(3, 'bhk/rk', df['bhk/rk'])
    df_num.insert(6, 'area_sqft', df['area_sqft'])
    df_num.insert(8, 'total_price', df['total_price'])

    # Removing outliers
    df_fil = pp.remove_outliers(df_num, ['total_price'], 10)

    # Model training
    X = df_fil.iloc[:, [2, 3, 4, 6, 7]]
    Y = df_fil.iloc[:, -1]
    model = LinearRegression()
    model.fit(X, Y)

    # Creating necessary directories
    catalog_dir: str = os.path.join('..', 'catalog')
    model_dir: str = os.path.join('..', 'model')

    os.mkdir(catalog_dir)
    os.mkdir(model_dir)

    # Saving the model
    with open(os.path.join(catalog_dir, 'catalog.json'), 'w') as catalog_writer:
        json.dump({
            'encoding_variables': encoding_variables,
            'encodings': encodings,
            'data_values': pp.get_values(df.to_dict()),
            'columns': X.columns.tolist()
        }, catalog_writer, indent=4)
    
    with open(os.path.join(model_dir, 'model.sav'), 'wb') as model_writer:
        pk.dump(model, model_writer)


if __name__ == "__main__":
    main()

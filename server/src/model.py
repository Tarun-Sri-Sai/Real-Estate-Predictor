from sklearn.linear_model import LinearRegression as sk_lr
from json import dump as json_dump
from pickle import dump as pk_dump
from pandas import DataFrame as pd_df
from preprocess import rename as pp_rename, strip as pp_strip, remove as pp_remove, title as pp_title

from preprocess import encode, create_encodings, get_values, string_cols, remove_outliers
from pandas import read_csv
from os import path, mkdir


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
    df: pd_df = read_csv(path.join('..', 'data', 'data.csv'))

    # Preprocessing the dataframe columns
    df = pp_rename(df, df.columns)
    df = pp_strip(df, string_cols(df))

    # Extracting plot type from BHK
    df.insert(4, 'plot_type', df['bhk'].apply(get_plot_type))
    df.insert(5, 'bhk/rk', df['bhk'].apply(get_bhk))

    # Removing unwanted columns
    df = pp_remove(df, ['unnamed_0', 'bhk'])

    # Adding title case
    df = pp_title(df, ['plot_type', 'construction_status', 'location'])

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
        encodings[column] = create_encodings(
            df[column], df['total_price'])

    # Creating a numeric dataframe
    df_num = pd_df()
    for column in encoding_variables:
        df_num[column] = encode(df[column], encodings[column])

    df_num.insert(3, 'bhk/rk', df['bhk/rk'])
    df_num.insert(6, 'area_sqft', df['area_sqft'])
    df_num.insert(8, 'total_price', df['total_price'])

    # Removing outliers
    df_fil = remove_outliers(df_num, ['total_price'], 10)

    # Model training
    X = df_fil.iloc[:, [2, 3, 4, 6, 7]]
    Y = df_fil.iloc[:, -1]
    model = sk_lr()
    model.fit(X, Y)

    # Creating necessary directories
    catalog_dir: str = path.join('..', 'catalog')
    model_dir: str = path.join('..', 'model')

    mkdir(catalog_dir)
    mkdir(model_dir)

    # Saving the model
    with open(path.join(catalog_dir, 'catalog.json'), 'w') as catalog_writer:
        json_dump({
            'encoding_variables': encoding_variables,
            'encodings': encodings,
            'data_values': get_values(df.to_dict()),
            'columns': X.columns.tolist()
        }, catalog_writer, indent=4)

    with open(path.join(model_dir, 'model.sav'), 'wb') as model_writer:
        pk_dump(model, model_writer)


if __name__ == "__main__":
    main()

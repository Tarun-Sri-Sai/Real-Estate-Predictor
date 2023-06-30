import pandas as pd
import numpy as np


def remove(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result: pd.DataFrame = pd.DataFrame()
    for column in df.columns:
        if column in columns:
            continue

        result[column] = df[column]

    return result


def snake_case(name: str) -> str:
    return '_'.join(name.strip().replace(':', '').lower().split(' '))


def rename(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result: pd.DataFrame = pd.DataFrame()
    for column in df.columns:
        if column not in columns:
            result[column] = df[columns]
            continue

        result[snake_case(column)] = df[column]
    
    return result


def string_cols(df: pd.DataFrame) -> list[str]:
    result: list[str] = [*filter(
        lambda x: df[x].dtype == 'object', df.columns)]
    return result


def strip(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result: pd.DataFrame = pd.DataFrame()
    for column in df.columns:
        if column not in columns:
            result[column] = df[column]
            continue

        result[column] = df[column].apply(lambda x: x.strip())
    
    return result


def title(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result: pd.DataFrame = pd.DataFrame()
    for column in df.columns:
        if column not in columns:
            result[column] = df[column]
            continue

        result[column] = df[column].apply(str.title)

    return result


def create_encodings(column: pd.Series, output: pd.Series):
    df_temp: pd.DataFrame = pd.DataFrame({'column': column, 'output': output})
    unique_categories: np.ndarray = df_temp['column'].unique()
    avg_prices: pd.Series = df_temp.groupby('column')['output'].mean()
    sorted_categories: list = list(sorted(
        unique_categories, key=lambda x: avg_prices[x]))
    encodings = {
        category: index for index, category in enumerate(sorted_categories)
    }
    return encodings


def encode(column: pd.Series, encodings: dict) -> pd.Series:
    return column.map(encodings)


def get_values(df: dict) -> dict:
    return {
        key: list(set(df[key].values())) for key, _  in df.items()
    }


def remove_outliers(df: pd.DataFrame, columns: list[str], min_count: int) -> pd.DataFrame:
    result: pd.DataFrame = df
    for column in columns:
        value_counts: dict = result[column].value_counts().to_dict()
        result = result[result[column].apply(
            lambda x: value_counts[x] >= min_count)]
        
    return result

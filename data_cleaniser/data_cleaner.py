from typing import Any, Dict

import pandas as pd
from pandas import DataFrame

def convert_year_column(data_frame: DataFrame) -> DataFrame:
    df = data_frame.copy()

    if 'year' in df.columns and df['year'].dtype == 'float64':
        df['year'] = pd.to_datetime(df['year'].astype(int), format='%Y').dt.date
    return df

def data_cleaner(dict_df: Dict[Any, DataFrame]) -> Dict[Any, DataFrame]:
    dicts_of_dfs = {}
    for count, df in enumerate(dict_df.values()):
        df = df.copy()
        # Drop columns with more than 50% NaN values
        threshold = int(len(df) * 0.5)
        df = df.dropna(axis=1, thresh=threshold)
        df = df.dropna(how='all')

        unnamed_cols = [col for col in df.columns if 'Unnamed' in col]

        df.drop(unnamed_cols, axis=1, inplace=True)

        # Regular expression pattern to match a narrow no-break space (NNBSP) followed by an asterisk
        pattern = r'[\u202F(\*|\s(?=%))|\u00A0]'

        for column in df.columns:
            if df[column].dtype == object:  # Only apply to columns with string data
                df[column] = df[column].str.replace(pattern, ' ', regex=True)

        dicts_of_dfs[count] = convert_year_column(df)

    return dicts_of_dfs

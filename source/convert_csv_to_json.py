from io import StringIO

import pandas as pd


def lambda_handler(event, context):
    pass


def csv_to_json(csv_string: str) -> str:
    dataframe = pd.read_csv(StringIO(csv_string))
    return dataframe.to_json(orient="records")

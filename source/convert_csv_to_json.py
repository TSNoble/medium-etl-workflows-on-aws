import boto3

import pandas as pd


def lambda_handler(event, _):
    s3_client = boto3.client("s3")
    file_stream = s3_client.get_object(Bucket=event["InputBucket"], Key=event["InputKey"])["Body"]
    json_data = csv_to_json(file_stream).encode("utf-8")
    s3_client.put_object(Bucket=event["OutputBucket"], Key=event["OutputKey"], Body=json_data)


def csv_to_json(file_obj) -> str:
    dataframe = pd.read_csv(file_obj)
    return dataframe.to_json(orient="records")

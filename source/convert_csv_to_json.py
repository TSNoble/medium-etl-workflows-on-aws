import boto3

import pandas as pd


def lambda_handler(event, _):
    s3_client = boto3.client("s3")
    csv_file = s3_client.get_object(Bucket=event["InputBucket"], Key=event["InputKey"])["Body"]
    json_data = csv_to_json(csv_file).encode("utf-8")
    s3_client.put_object(Bucket=event["OutputBucket"], Key=event["OutputKey"], Body=json_data)


def csv_to_json(csv_file) -> str:
    dataframe = pd.read_csv(csv_file)
    return dataframe.to_json(orient="records")

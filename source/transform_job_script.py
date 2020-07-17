import boto3
from io import StringIO


def transform_file_local(src_bucket, dest_bucket, file_key):
    s3_client = boto3.client("s3")
    file_stream = s3_client.get_object(Bucket=src_bucket, Key=file_key)["Body"]
    file_contents = file_stream.read().decode("utf-8")
    file_contents.replace("Hello, World!", "Greetings, Planet!")
    s3_client.put_object(Bucket=dest_bucket, Key=file_key, Body=StringIO(file_contents))

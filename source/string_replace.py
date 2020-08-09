import boto3


def lambda_handler(event, _):
    s3_client = boto3.client("s3")
    input_file = s3_client.get_object(Bucket=event["InputBucket"], Key=event["InputKey"])["Body"]
    replaced_string = replace_string(input_file, event["ToReplace"], event["ReplaceWith"]).encode("utf-8")
    s3_client.put_object(Bucket=event["OutputBucket"], Key=event["OutputKey"], Body=replaced_string)


def replace_string(file, to_replace: str, replace_with: str) -> str:
    file_contents = file.read().decode("utf-8")
    return file_contents.replace(to_replace, replace_with)


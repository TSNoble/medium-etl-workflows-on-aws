import json
from pathlib import Path

import jmespath
import pytest
import boto3
import botocore.exceptions


DATA_DIR = Path(__file__).parent.parent.parent.joinpath("data")


def get_stack_output(key: str):
    stack_outputs_file = Path(__file__).parent.parent.parent.joinpath("stack-outputs.json")
    with open(stack_outputs_file, "r") as stack_outputs:
        stack_outputs_json = json.load(stack_outputs)
    return jmespath.search(f"[?OutputKey == '{key}'].OutputValue | [0]", stack_outputs_json)


def object_exists(bucket: str, key: str):
    s3_resource = boto3.resource("s3")
    try:
        s3_resource.Object(bucket, key).load()
        return True
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise


@pytest.fixture(scope="module")
def mock_files():
    s3_client = boto3.client("s3")
    s3_resource = boto3.resource("s3")
    source_bucket_name = get_stack_output("SourceBucketName")
    processing_bucket_name = get_stack_output("ProcessingBucketName")
    destination_bucket_name = get_stack_output("DestinationBucketName")
    s3_client.put_object(Bucket=source_bucket_name, Key="file1", Body="")
    s3_client.put_object(Bucket=source_bucket_name, Key="file2", Body="")
    s3_client.upload_file(Bucket=source_bucket_name, Key="people.csv", Filename=str(DATA_DIR/"people.csv"))
    s3_client.upload_file(Bucket=source_bucket_name, Key="jobs.csv", Filename=str(DATA_DIR/"jobs.csv"))
    s3_client.upload_file(Bucket=processing_bucket_name, Key="string_replace/people.csv", Filename=str(DATA_DIR/"people.csv"))
    s3_client.upload_file(Bucket=processing_bucket_name, Key="string_replace/jobs.csv", Filename=str(DATA_DIR / "jobs.csv"))
    s3_client.upload_file(Bucket=processing_bucket_name, Key="calculate_total_earnings/merged.csv", Filename=str(DATA_DIR/"merged.csv"))
    yield
    s3_resource.Bucket(source_bucket_name).objects.all().delete()
    s3_resource.Bucket(processing_bucket_name).objects.all().delete()
    s3_resource.Bucket(destination_bucket_name).objects.all().delete()


@pytest.mark.parametrize(
    "required_files, expected_result",
    [
        ([], True),
        (["file1"], True),
        (["file3"], False),
        (["file1", "file2"], True),
        (["file1", "file3"], False),
        (["file1", "file2", "file3"], False)
    ]
)
def test_check_workflow_ready_lambda(mock_files, required_files, expected_result):
    lambda_client = boto3.client("lambda")
    event = {
        "InputBucket": get_stack_output("SourceBucketName"),
        "RequiredFiles": required_files
    }
    function_name = get_stack_output("CheckWorkflowReadyLambda")
    response = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(event))
    assert response["StatusCode"] == 200
    assert json.load(response["Payload"]) == expected_result


@pytest.mark.parametrize(
    "input_key, expected_file",
    [
        ("people.csv", "people_string_replaced.csv"),
        ("jobs.csv", "jobs_string_replaced.csv")
    ]
)
def test_string_replace_lambda(mock_files, input_key, expected_file):
    lambda_client = boto3.client("lambda")
    event = {
        "InputBucket": get_stack_output("SourceBucketName"),
        "InputKey": input_key,
        "ToReplace": "Programming",
        "ReplaceWith": "Coding",
        "OutputBucket": get_stack_output("ProcessingBucketName"),
        "OutputKey": f"string_replace/{input_key}"
    }
    function_name = get_stack_output("StringReplaceLambda")
    response = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(event))
    assert response["StatusCode"] == 200
    assert object_exists(bucket=event["OutputBucket"], key=event["OutputKey"])


def test_calculate_total_earnings_lambda(mock_files):
    lambda_client = boto3.client("lambda")
    event = {
        "InputBucket": get_stack_output("ProcessingBucketName"),
        "PeopleKey": "string_replace/people.csv",
        "JobsKey": "string_replace/jobs.csv",
        "OutputBucket": get_stack_output("ProcessingBucketName"),
        "OuputKey": "calculate_total_earnings/merged.csv"
    }
    function_name = get_stack_output("CalculateTotalEarningsLambda")
    response = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(event))
    assert response["StatusCode"] == 200
    assert object_exists(bucket=event["OutputBucket"], key=event["OutputKey"])


def test_convert_csv_to_json_lambda(mock_files):
    lambda_client = boto3.client("lambda")
    event = {
        "InputBucket": get_stack_output("ProcessingBucketName"),
        "InputKey": "calculate_total_earnings/merged.csv",
        "OutputBucket": get_stack_output("DestinationBucketName"),
        "OutputKey": f"output.json"
    }
    function_name = get_stack_output("ConvertCsvToJsonLambda")
    response = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(event))
    assert response["StatusCode"] == 200
    assert object_exists(bucket=event["OutputBucket"], key=event["OutputKey"])

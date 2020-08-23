import moto
import boto3
import pytest


@pytest.fixture
def mock_s3():
    with moto.mock_s3():
        mock_s3 = boto3.client("s3")
        mock_s3.create_bucket(Bucket="MockInputBucket")
        mock_s3.create_bucket(Bucket="MockOutputBucket")
        yield mock_s3

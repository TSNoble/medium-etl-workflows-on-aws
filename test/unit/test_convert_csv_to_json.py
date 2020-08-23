import json
from io import StringIO

import pytest

from source.convert_csv_to_json import csv_to_json, lambda_handler


@pytest.mark.parametrize(
    "csv_data, expected_json",
    [
        ("FOO", []),
        ("FOO,BAR,BAZ", []),
        ("FOO,BAR,BAZ\n1,2,3", [{"FOO": 1, "BAR": 2, "BAZ": 3}]),
        ("FOO,BAR,BAZ\n1,two,3.0\n4,five,6.0", [{"FOO": 1, "BAR": "two", "BAZ": 3.0}, {"FOO": 4, "BAR": "five", "BAZ": 6.0}])
    ]
)
def test_csv_to_json(csv_data, expected_json):
    csv_file_buffer = StringIO(csv_data)
    assert csv_to_json(csv_file_buffer) == json.dumps(expected_json, separators=(",", ":"))


def test_lambda_handler(mock_s3):
    event = {
        "InputBucket": "MockInputBucket",
        "InputKey": "input_file.csv",
        "OutputBucket": "MockOutputBucket",
        "OutputKey": "csv_to_json/output_file.json"
    }
    mock_s3.put_object(Bucket=event["InputBucket"], Key=event["InputKey"], Body="FOO,BAR,BAZ\n1,2,3")
    lambda_handler(event, [])
    file_bytes = mock_s3.get_object(Bucket=event["OutputBucket"], Key=event["OutputKey"])["Body"]
    assert file_bytes.read().decode("utf-8") == json.dumps([{"FOO": 1, "BAR": 2, "BAZ": 3}], separators=(",", ":"))

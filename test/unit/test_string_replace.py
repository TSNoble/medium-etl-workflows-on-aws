from io import BytesIO

import pytest

from source.string_replace import replace_string, lambda_handler


@pytest.mark.parametrize(
    "input_string, to_replace, replace_with, expected_string",
    [
        (b"", "", "", ""),
        (b"Foo", "", "", "Foo"),
        (b"Foo", "Foo", "Bar", "Bar"),
        (b"Foo, Foo, Foo", "Foo", "Bar", "Bar, Bar, Bar"),
        (b"Foo, Baz, Foo", "Foo", "Bar", "Bar, Baz, Bar")
    ]
)
def test_replace_string(input_string, to_replace, replace_with, expected_string):
    input_string_buffer = BytesIO(input_string)
    assert replace_string(input_string_buffer, to_replace, replace_with) == expected_string


def test_lambda_handler(mock_s3):
    event = {
        "InputBucket": "MockInputBucket",
        "InputKey": "input_file.csv",
        "OutputBucket": "MockOutputBucket",
        "OutputKey": "string_replace/output_file.csv",
        "ToReplace": "Foo",
        "ReplaceWith": "Bar"
    }
    mock_s3.put_object(Bucket=event["InputBucket"], Key=event["InputKey"], Body="Foo, Bar, Baz")
    lambda_handler(event, [])
    file_bytes = mock_s3.get_object(Bucket=event["OutputBucket"], Key=event["OutputKey"])["Body"]
    assert file_bytes.read().decode("utf-8") == "Bar, Bar, Baz"

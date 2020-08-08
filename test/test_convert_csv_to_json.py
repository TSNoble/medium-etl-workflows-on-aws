import json
import pytest

from source.convert_csv_to_json import csv_to_json


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
    assert csv_to_json(csv_data) == json.dumps(expected_json, separators=(",", ":"))

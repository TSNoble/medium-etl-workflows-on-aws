from io import BytesIO

import pytest

from source.string_replace import replace_string


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


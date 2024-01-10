import pytest

from northpole.parsers import string_parser


@pytest.mark.parametrize(
    "data,expected", [("Santa", "Santa"), ("NorthPole\n", "NorthPole")]
)
def test_string_parser(data: str, expected: str) -> None:
    assert string_parser(data) == expected

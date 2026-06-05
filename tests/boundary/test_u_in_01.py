# U-IN-01 | FR-05

import pytest


def test_u_in_01_empty_input_rejects_format_error():
    # U-IN-01
    # Given
    user_input = ""

    # When
    from unit_converter.boundary.input_parser import parse

    parse(user_input)

    # Then
    pytest.fail("RED: U-IN-01 — 구현 없음")

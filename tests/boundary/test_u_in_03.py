# U-IN-03 | FR-04

import pytest


def test_u_in_03_negative_value_rejected():
    # U-IN-03
    # Given
    user_input = "meter:-1"

    # When
    from unit_converter.boundary.input_parser import parse

    parse(user_input)

    # Then
    pytest.fail("RED: U-IN-03 — 구현 없음")

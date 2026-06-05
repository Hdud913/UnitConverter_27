# U-IN-02 | FR-05

import pytest


def test_u_in_02_missing_colon_rejects_format_error():
    # U-IN-02
    # Given
    user_input = "meter"

    # When
    from unit_converter.boundary.input_parser import parse

    parse(user_input)

    # Then
    pytest.fail("RED: U-IN-02 — 구현 없음")

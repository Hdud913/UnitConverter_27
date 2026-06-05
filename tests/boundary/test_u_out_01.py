# U-OUT-01 | FR-01, FR-02

from unittest.mock import MagicMock, patch

import pytest


def test_u_out_01_meter_2_5_emits_at_least_three_lines():
    # U-OUT-01
    # Given
    user_input = "meter:2.5"
    mock_results = {
        "meter": "2.5",
        "feet": "8.20210",
        "yard": "2.734025",
    }
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = mock_results

    # When
    with patch(
        "unit_converter.control.convert_use_case.ConvertUseCase",
        return_value=mock_use_case,
    ):
        from unit_converter.cli import run

        run(user_input)

    # Then
    pytest.fail("RED: U-OUT-01 — 구현 없음")

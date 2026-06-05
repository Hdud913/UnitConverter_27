"""Track A — UI/Boundary (CLI, 입력 검증, 출력 형식)."""

import pytest


def test_u_in_01_empty_input_rejects_format_error():
    # U-IN-01
    # Given
    user_input = ""

    # When
    # CLI 경계: 빈 입력 실행 (GREEN: subprocess 또는 input_parser 연동)

    # Then
    pytest.fail("RED: U-IN-01 — 구현 없음")


def test_u_in_02_missing_colon_rejects_format_error():
    # U-IN-02
    # Given
    user_input = "meter"

    # When
    # CLI 경계: 콜론 없는 입력 실행

    # Then
    pytest.fail("RED: U-IN-02 — 구현 없음")


def test_u_in_03_negative_value_rejected():
    # U-IN-03
    # Given
    user_input = "meter:-1"

    # When
    # CLI 경계: 음수 입력 실행

    # Then
    pytest.fail("RED: U-IN-03 — 구현 없음")


def test_u_out_01_meter_2_5_emits_at_least_three_lines():
    # U-OUT-01
    # Given
    user_input = "meter:2.5"

    # When
    # CLI 경계: 유효 입력 실행 후 stdout 수집

    # Then
    pytest.fail("RED: U-OUT-01 — 구현 없음")

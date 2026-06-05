"""Track B — Domain/Logic (변환 정확도, registry, 설정 로드)."""

import pytest


def test_d_cnv_01_feet_to_meter():
    # D-CNV-01
    # Given
    value_feet = 1
    expected_meters = 0.3048
    epsilon = 1e-4

    # When
    # LengthUnit.to_meter(value) — 1 feet → meter (GREEN: domain/length_unit)

    # Then
    pytest.fail("RED: D-CNV-01 — 구현 없음")


def test_d_cnv_02_convert_all_meter_to_feet_five_decimals():
    # D-CNV-02
    # Given
    source_unit = "meter"
    value = 2.5
    expected_feet = "8.20210"

    # When
    # Converter.convert_all(source_unit, value) — feet 결과 5자리

    # Then
    pytest.fail("RED: D-CNV-02 — 구현 없음")


def test_d_cnv_03_feet_to_yard_via_meter():
    # D-CNV-03
    # Given
    source_unit = "feet"
    value = 10

    # When
    # convert_all("feet", value)["yard"] == meter 경유 2단계 결과

    # Then
    pytest.fail("RED: D-CNV-03 — 구현 없음")


def test_d_reg_01_register_cubit_enables_conversion():
    # D-REG-01
    # Given
    unit_name = "cubit"
    meters_per_unit = 0.4572

    # When
    # Registry.register(unit_name, meters_per_unit) 후 convert_all("cubit", 1)

    # Then
    pytest.fail("RED: D-REG-01 — 구현 없음")


def test_d_cfg_01_broken_json_raises_config_error():
    # D-CFG-01
    # Given
    broken_config_path = "broken_units.json"

    # When
    # load_units_config(broken_config_path) — 깨진 JSON 로드

    # Then
    pytest.fail("RED: D-CFG-01 — 구현 없음")

# D-CNV-01 | FR-02, NFR-01

import pytest


def test_d_cnv_01_feet_to_meter():
    # D-CNV-01
    # Given
    value_feet = 1
    expected_meters = 0.3048
    epsilon = 1e-4

    # When
    from unit_converter.entity.length_unit import LengthUnit

    result = LengthUnit.from_name("feet").to_meter(value_feet)

    # Then
    assert abs(result - expected_meters) < epsilon

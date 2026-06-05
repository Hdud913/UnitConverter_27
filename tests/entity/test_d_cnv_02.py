# D-CNV-02 | FR-02, NFR-01

import pytest


def test_d_cnv_02_convert_all_meter_to_feet_five_decimals():
    # D-CNV-02
    # Given
    source_unit = "meter"
    value = 2.5
    expected_feet = "8.20210"

    # When
    from unit_converter.entity.converter import Converter
    from unit_converter.entity.unit_registry import default_registry

    results = Converter(default_registry()).convert_all(source_unit, value)

    # Then
    assert results["feet"] == expected_feet

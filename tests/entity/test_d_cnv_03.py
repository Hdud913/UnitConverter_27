# D-CNV-03 | FR-02, NFR-01

import pytest


def test_d_cnv_03_feet_to_yard_via_meter():
    # D-CNV-03
    # Given
    source_unit = "feet"
    value = 10

    # When
    from unit_converter.entity.converter import Converter
    from unit_converter.entity.unit_registry import default_registry

    Converter(default_registry()).convert_all(source_unit, value)

    # Then
    pytest.fail("RED: D-CNV-03 — 구현 없음")

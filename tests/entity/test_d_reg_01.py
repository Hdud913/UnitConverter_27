# D-REG-01 | EXT-02, NFR-01

import pytest


def test_d_reg_01_register_cubit_enables_conversion():
    # D-REG-01
    # Given
    unit_name = "cubit"
    meters_per_unit = 0.4572

    # When
    from unit_converter.entity.converter import Converter
    from unit_converter.entity.unit_registry import default_registry

    registry = default_registry()
    registry.register(unit_name, meters_per_unit)
    Converter(registry).convert_all("cubit", 1)

    # Then
    pytest.fail("RED: D-REG-01 — 구현 없음")

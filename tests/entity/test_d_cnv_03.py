# D-CNV-03 | FR-02, NFR-01

import json
from pathlib import Path

import pytest

_UNITS_JSON = Path(__file__).resolve().parent.parent.parent / "units.json"


def test_d_cnv_03_feet_to_yard_via_meter():
    # D-CNV-03
    # Given
    source_unit = "feet"
    value = 10
    epsilon = 1e-9

    with open(_UNITS_JSON, encoding="utf-8") as f:
        ratios = json.load(f)
    meters = value / ratios["meter_to_feet"]
    expected_yard = meters * ratios["meter_to_yard"]

    # When
    from unit_converter.entity.converter import Converter
    from unit_converter.entity.unit_registry import default_registry

    results = Converter(default_registry()).convert_all(source_unit, value)
    actual_yard = float(results["yard"])

    # Then
    assert abs(actual_yard - expected_yard) < epsilon

# D-CFG-01 | EXT-01

import pytest


def test_d_cfg_01_broken_json_raises_config_error():
    # D-CFG-01
    # Given
    broken_config_path = "broken_units.json"

    # When / Then
    from unit_converter.infrastructure.config_loader import ConfigError, load_units_config

    with pytest.raises(ConfigError):
        load_units_config(broken_config_path)

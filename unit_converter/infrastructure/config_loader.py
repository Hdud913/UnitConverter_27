import json


class ConfigError(Exception):
    pass


def load_units_config(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        raise ConfigError(str(exc)) from exc

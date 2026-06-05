import json
from dataclasses import dataclass
from pathlib import Path

_UNITS_JSON = Path(__file__).resolve().parent.parent.parent / "units.json"


def _load_ratios() -> dict[str, float]:
    with open(_UNITS_JSON, encoding="utf-8") as f:
        return json.load(f)


@dataclass(frozen=True)
class LengthUnit:
    name: str
    meters_per_unit: float

    def to_meter(self, value: float) -> float:
        return value * self.meters_per_unit

    @classmethod
    def from_name(cls, name: str) -> "LengthUnit":
        ratios = _load_ratios()
        if name == "meter":
            return cls("meter", 1.0)
        if name == "feet":
            return cls("feet", 1.0 / ratios["meter_to_feet"])
        if name == "yard":
            return cls("yard", 1.0 / ratios["meter_to_yard"])
        raise ValueError(f"Unknown unit: {name}")

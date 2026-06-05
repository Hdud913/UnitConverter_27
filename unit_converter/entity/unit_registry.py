from unit_converter.entity.length_unit import LengthUnit


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, LengthUnit] = {}

    def register(self, name: str, meters_per_unit: float) -> None:
        self._units[name] = LengthUnit(name, meters_per_unit)

    def get(self, name: str) -> LengthUnit:
        return self._units[name]

    def all_units(self) -> list[LengthUnit]:
        return list(self._units.values())


def default_registry() -> UnitRegistry:
    registry = UnitRegistry()
    for name in ("meter", "feet", "yard"):
        unit = LengthUnit.from_name(name)
        registry.register(unit.name, unit.meters_per_unit)
    return registry

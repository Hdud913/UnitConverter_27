from unit_converter.entity.unit_registry import UnitRegistry


class Converter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert_all(self, source_unit: str, value: float) -> dict[str, str]:
        source = self._registry.get(source_unit)
        meters = source.to_meter(value)
        results: dict[str, str] = {}
        for unit in self._registry.all_units():
            converted = meters / unit.meters_per_unit
            if unit.name == "feet":
                results[unit.name] = f"{converted:.5f}"
            else:
                results[unit.name] = str(converted)
        return results

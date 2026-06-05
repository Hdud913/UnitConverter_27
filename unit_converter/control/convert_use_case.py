from unit_converter.entity.converter import Converter
from unit_converter.entity.unit_registry import default_registry


class ConvertUseCase:
    def __init__(self, converter: Converter | None = None) -> None:
        self._converter = converter or Converter(default_registry())

    def execute(self, unit: str, value: float) -> dict[str, str]:
        return self._converter.convert_all(unit, value)

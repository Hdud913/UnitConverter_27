from unit_converter.boundary.input_parser import parse
from unit_converter.boundary.output_formatter import format_table
from unit_converter.control.convert_use_case import ConvertUseCase


def run(user_input: str) -> None:
    unit, value = parse(user_input)
    use_case = ConvertUseCase()
    results = use_case.execute(unit, value)
    print(format_table(unit, value, results))

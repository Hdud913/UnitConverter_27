class ParseError(Exception):
    pass


_FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"


def parse(user_input: str) -> tuple[str, float]:
    if not user_input:
        raise ParseError(_FORMAT_ERROR)

    unit, value_str = user_input.split(":", 1)
    value = float(value_str)
    return unit, value

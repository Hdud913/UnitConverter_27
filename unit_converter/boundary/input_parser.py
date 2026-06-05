class ParseError(Exception):
    pass


_FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"


def parse(user_input: str) -> tuple[str, float]:
    if not user_input or ":" not in user_input:
        raise ParseError(_FORMAT_ERROR)

    unit, value_str = user_input.split(":", 1)
    if not unit or not value_str:
        raise ParseError(_FORMAT_ERROR)

    try:
        value = float(value_str)
    except ValueError as exc:
        raise ParseError(_FORMAT_ERROR) from exc

    if value < 0:
        raise ParseError("Negative values are not allowed")

    return unit, value

def format_table(source_unit: str, source_value: float, results: dict[str, str]) -> str:
    lines = [
        f"{source_value} {source_unit} = {converted} {target_unit}"
        for target_unit, converted in results.items()
    ]
    return "\n".join(lines)

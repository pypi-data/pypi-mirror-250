from dbnomics_data_model.validation.errors.validation_error_code import ValidationErrorCode


def parse_csv_str(value: str) -> list[str]:
    """Split a string with comma-separated values to a list of strings."""
    value = value.strip()
    return [stripped_word for word in value.split(",") if (stripped_word := word.strip())]


def parse_validation_error_codes(value: str) -> set[ValidationErrorCode]:
    words = parse_csv_str(value)
    return {ValidationErrorCode.parse(word) for word in words}

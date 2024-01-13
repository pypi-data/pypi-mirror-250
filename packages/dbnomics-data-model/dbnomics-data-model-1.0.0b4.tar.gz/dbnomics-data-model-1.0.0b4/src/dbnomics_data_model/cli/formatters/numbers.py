def format_delta(old_value: float, new_value: float) -> str:
    delta = new_value - old_value

    if delta > 0:
        return f"+{delta}"

    return str(delta)

def format_number(number):
    number = float(number)

    if abs(number) < 1000:
        return f"{number:.2f}".rstrip("0").rstrip(".")

    return f"{int(number):,}"
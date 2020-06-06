from decimal import Decimal


def to_decimal(num) -> Decimal:
    return round(Decimal(num), 3)


def display(model_object, attr):
    display_attr = f'get_{attr}_display'

    if hasattr(model_object, display_attr):
        return getattr(model_object, display_attr)()
    return getattr(model_object, attr)

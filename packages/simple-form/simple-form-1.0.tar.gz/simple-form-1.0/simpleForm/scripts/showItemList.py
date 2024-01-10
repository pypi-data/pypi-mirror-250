from .ternaryOperator import ternaryOperator

def showItemList(count: int, spacing: int, orderedList: bool):
    assert isinstance(count, int), f"The count must be an integer."
    assert isinstance(spacing, int), f"The spacing must be an integer."
    assert isinstance(orderedList, bool), f"The orderedList must be a boolean."

    return f"{ spacing * " " }{ ternaryOperator( orderedList, f"{ count }.", "-" ) }"
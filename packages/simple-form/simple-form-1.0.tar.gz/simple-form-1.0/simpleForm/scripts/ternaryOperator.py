def ternaryOperator(condition: bool, trueVal, falseVal):
    assert isinstance(condition, bool), "Condition must be a boolean"
    return trueVal if condition else falseVal
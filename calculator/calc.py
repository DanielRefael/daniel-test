class CalculationError(Exception):
    """A calculation request that cannot return a result."""


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculationError("a number is missing or is not a number")
    return value


def calculate(operation, a, b):
    left = _number(a)
    right = _number(b)
    if operation == "add":
        return left + right
    if operation == "subtract":
        return left - right
    if operation == "multiply":
        return left * right
    if operation == "divide":
        if right == 0:
            raise CalculationError("divide by zero")
        return left / right
    raise CalculationError("unknown operation")

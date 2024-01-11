# simple_math.py


def add(x, y):
    """
    Adds two numbers.Q

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return x + y


def subtract(x, y):
    """
    Subtracts two numbers and returns the result.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The difference between x and y.
    """
    return x - y


def multiply(x, y):
    """
    Multiplies two numbers and returns the result.

    Parameters:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The product of x and y.
    """
    return x * y


def divide(x, y):
    """
    Divides two numbers and returns the result.

    Parameters:
        x (float): The numerator.
        y (float): The denominator.

    Returns:
        float: The result of the division.

    Raises:
        ValueError: If the denominator is zero.
    """
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

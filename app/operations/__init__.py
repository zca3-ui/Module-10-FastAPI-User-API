
from typing import Union

# Define the types of numbers accepted by the calculator
Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers
    """
    result = a + b
    return result


def subtract(a: Number, b: Number) -> Number:
    """
    Subtract the second number from the first.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference between the two numbers
    """
    result = a - b
    return result


def multiply(a: Number, b: Number) -> Number:
    """
    Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of the two numbers
    """
    result = a * b
    return result


def divide(a: Number, b: Number) -> float:
    """
    Divide the first number by the second.

    Args:
        a: First number
        b: Second number

    Returns:
        Quotient of the two numbers

    Raises:
        ValueError: If the second number is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero!")

    result = a / b
    return result

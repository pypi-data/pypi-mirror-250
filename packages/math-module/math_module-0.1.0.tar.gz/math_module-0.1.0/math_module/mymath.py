def gcd(a, b):
    """
    Calculates the greatest common divisor (GCD) of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The GCD of the two numbers.
    """
    if (b == 0):
        return a
    return gcd(b, a % b)


def lcm(a, b):
    """
    Calculate the least common multiple (LCM) of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The LCM of the two numbers.
    """
    result = (a*b)/gcd(a, b)
    return result

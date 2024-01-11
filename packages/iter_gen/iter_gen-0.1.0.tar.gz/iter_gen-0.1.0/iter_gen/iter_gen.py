"""
This module contains functions for generating iterator
that yields numbers up to a given number.
"""


def odd_gen(n: int):
    """
    Generate an iterator that yields odd numbers up to a given number.

    Parameters:
        n (int): The upper limit of the range to generate odd numbers.

    Yields:
        int: The next odd number in the range.
    """
    # Iterate over the range from 1 to n (exclusive) with a step of 2
    for i in range(1, n, 2):
        # Yield the current odd number
        yield i


def even_gen(n: int):
    """
    Generate an iterator that yields even numbers up to a given number.

    Parameters:
        n (int): The upper limit of the range to generate even numbers.

    Yields:
        int: The next even number in the range.
    """
    # Iterate over the range from 1 to n (exclusive) with a step of 2
    for i in range(0, n, 2):
        # Yield the current even number
        yield i


def prime_gen(n: int):
    """
    Generate an iterator that yields prime numbers up to a given number.

    Parameters:
        n (int): The upper limit of the range to generate prime numbers.

    Yields:
        int: The next prime number in the range.
    """
    # Iterate over the range from 2 to n
    for i in range(2, n):
        # Check if the current number is a prime number
        if all(i % j != 0 for j in range(2, i)):
            # Yield the current prime number
            yield i


def custom_gen(start: int, end: int, step: int):
    """
    Generate an iterator that yields numbers in a custom range.

    Parameters:
        start (int): The starting number of the range.
        end (int): The ending number of the range.
        step (int): The step size of the range.

    Yields:
        int: The next number in the range.
    """
    # Iterate over the range from start to end (exclusive) with the given step
    for i in range(start, end, step):
        # Yield the current number
        yield i

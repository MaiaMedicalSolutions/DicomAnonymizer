"""
Utility for printing the tags in the original hex format.
"""


def string_to_hex(s: str) -> hex:
    """
    Convert a hex string to its original hex number.
    Args:
        s (str): hex string
    Returns:
        hex: hex number
    """
    return int(s, 16)


def hex_to_string(x):
    """
    Convert a tag number to its original hex string. E.g. if a tag has the hex number 0x0008, it becomes 8, and we then
    convert it back to 0x0008 (as a string).
    Args:
        x (hex): hex number
    Returns:
        str: hex string
    """
    x = str(hex(x))
    left = x[:2]
    right = x[2:]
    num_zeroes = 4 - len(right)
    return left + ('0' * num_zeroes) + right


def tag_to_hex_strings(tag):
    """
    Convert a tag tuple to a tuple of full hex number strings.
    E.g. (0x0008, 0x0010) is evaluated as (8, 16) by python. So
    we convert it back to a string '(0x0008, 0x0010)' for pretty printing.
    Args:
        tag (tuple): tag tuple
    Returns:
        tuple: tuple of full hex number strings
    """
    return tuple([hex_to_string(tag_element) for tag_element in tag])

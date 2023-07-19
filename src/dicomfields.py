import json
from typing import Tuple, List

from src.format_tag import string_to_hex

tags = json.load(open("./data/dicom_fields_latest.json"))


def _generate_hex_tags(number_of_places=2):
    """ Generate all possible hexadecimal values with a given number of places
    Args:
        number_of_places (int): number of places of the hexadecimal value
    Returns:
        generator: generator of hexadecimal values
    """
    for i in range(0, 16 ** number_of_places):
        i_hex = format(i, '02x')
        yield i_hex


def _generate_single_hex_tags_with_xxxx(number_of_places=4):
    """ Generate all possible hexadecimal values with a given number of places
    Args:
        stag (str): tag to generate
        number_of_places (int): number of places of the hexadecimal value
    Returns:
        generator: generator of hexadecimal values
    """
    first_tags = []
    for i_hex in _generate_hex_tags(number_of_places):
        first_tags.append(string_to_hex("0x" + i_hex))
    return first_tags


def _generate_single_hex_tags_with_xx(stag: str, number_of_places=2):
    """ Generate all possible hexadecimal values with a given number of places
    Args:
        stag (str): tag to generate
        number_of_places (int): number of places of the hexadecimal value
    Returns:
        generator: generator of hexadecimal values
    """
    first_tags = []
    if stag.find("xx") != -1:
        for i_hex in _generate_hex_tags(number_of_places):
            first_tags.append(string_to_hex(stag.replace("xx", i_hex)))
    else:
        first_tags.append(string_to_hex(stag))
    return first_tags


def generate_xx_tags(tag: List[str]) -> List[Tuple[hex, hex]]:
    """ Get a dicom tag filled with placeholder xx values and generate all possible tags
    Args:
        tag (list): list of two strings representing the tag
    Returns:
        list: list of tuples of hexadecimal values
    """

    assert tag[0].find("xx") != -1 or tag[1].find("xx") != -1

    if tag[0].find("0xxxxx") != -1:
        first_tags = _generate_single_hex_tags_with_xxxx(4)
    else:
        first_tags = _generate_single_hex_tags_with_xx(tag[0], 2)

    if tag[1].find("0xxxxx") != -1:
        second_tags = _generate_single_hex_tags_with_xxxx(4)
    else:
        second_tags = _generate_single_hex_tags_with_xx(tag[1], 2)

    tag_list = []
    for first_tag in first_tags:
        for second_tag in second_tags:
            tag_list.append((first_tag, second_tag))

    return tag_list


def convert_tags(dtags: list) -> List[Tuple[hex, hex]]:
    """Converts the tags from the json file to a list of tuples of hex values
    Args:
        dtags (list): list of tags from the json file
    Returns:
        list: list of tuples of hexadecimal values

    """

    tag_list = []

    for elem in dtags:

        if elem["tag"][0].find("0xgggg") != -1 or elem["tag"][1].find("0xgggg") != -1:
            print(elem)
            continue

        if elem["tag"][0].find("xx") == -1 and elem["tag"][1].find("xx") == -1:
            tag_list.append((string_to_hex(elem["tag"][0]), string_to_hex(elem["tag"][1])))
            continue
        else:
            tag_list.extend(generate_xx_tags(elem["tag"]))
            continue

        # Last element is {'tag': ['0xgggg', '0xeeee'], 'info': 'special:`where gggg is odd`', 'name': 'Private Attributes'}
        # Handled in `anonymize_dataset` function

    # remove duplicates
    tag_list = list(set(tag_list))

    return tag_list


D_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["D_TAGS"])
Z_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["Z_TAGS"])
X_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["X_TAGS"])
U_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["U_TAGS"])
Z_D_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["Z_D_TAGS"])
X_Z_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["X_Z_TAGS"])
X_D_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["X_D_TAGS"])
X_Z_D_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["X_Z_D_TAGS"])
X_Z_U_STAR_TAGS: List[Tuple[hex, hex]] = convert_tags(tags["X_Z_U_STAR_TAGS"])

ALL_TAGS: List[Tuple[hex, hex]] = []
ALL_TAGS.extend(D_TAGS)
ALL_TAGS.extend(Z_TAGS)
ALL_TAGS.extend(X_TAGS)
ALL_TAGS.extend(U_TAGS)
ALL_TAGS.extend(Z_D_TAGS)
ALL_TAGS.extend(X_Z_TAGS)
ALL_TAGS.extend(X_D_TAGS)
ALL_TAGS.extend(X_Z_D_TAGS)
ALL_TAGS.extend(X_Z_U_STAR_TAGS)

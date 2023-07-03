import json

from src.format_tag import string_to_hex

tags = json.load(open("./data/dicom_fields_latest.json"))


def convert_tags(dtags: list) -> list:
    """Converts the tags from the json file to a list of tuples of hex values
    Args:
        dtags (list): list of tags from the json file
    Returns:
        list: list of tuples of hexadecimal values

    """
    return [
        (string_to_hex(elem["tag"][0]), string_to_hex(elem["tag"][1]))
        for elem in dtags
        if elem["tag"][0].find("xx") == -1 and elem["tag"][1].find("xx") == -1
    ]


D_TAGS: list = convert_tags(tags["D_TAGS"])
Z_TAGS: list = convert_tags(tags["Z_TAGS"])
X_TAGS: list = convert_tags(tags["X_TAGS"])
U_TAGS: list = convert_tags(tags["U_TAGS"])
Z_D_TAGS: list = convert_tags(tags["Z_D_TAGS"])
X_Z_TAGS: list = convert_tags(tags["X_Z_TAGS"])
X_D_TAGS: list = convert_tags(tags["X_D_TAGS"])
X_Z_D_TAGS: list = convert_tags(tags["X_Z_D_TAGS"])
X_Z_U_STAR_TAGS: list = convert_tags(tags["X_Z_U_STAR_TAGS"])

ALL_TAGS = []
ALL_TAGS.extend(D_TAGS)
ALL_TAGS.extend(Z_TAGS)
ALL_TAGS.extend(X_TAGS)
ALL_TAGS.extend(U_TAGS)
ALL_TAGS.extend(Z_D_TAGS)
ALL_TAGS.extend(X_Z_TAGS)
ALL_TAGS.extend(X_D_TAGS)
ALL_TAGS.extend(X_Z_D_TAGS)
ALL_TAGS.extend(X_Z_U_STAR_TAGS)

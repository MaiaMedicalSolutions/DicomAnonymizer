import os

import pydicom


def get_private_tag(dataset, tag):
    """
    Get the creator and element from tag
    Args:
        dataset: pydicom dataset
        tag: tag to get private creator and element
    Returns:
        private_tag: private tag with creator and element
    """
    element = dataset.get(tag)

    element_value = element.value
    tag_group = element.tag.group
    # The element is a private creator
    if element_value in dataset.private_creators(tag_group):
        return {"creator": {"tagGroup": tag_group, "creatorName": element.value}, "element": None}
    # The element is a private element with an associated private creator
    else:
        # Shift the element tag in order to get the create_tag 0x1009 >> 8 will give 0x0010
        create_tag_element = element.tag.element >> 8
        create_tag = pydicom.tag.Tag(tag_group, create_tag_element)
        create_dataset = dataset.get(create_tag)
        # Define which offset should be applied to the creator to find this element 0x0010 << 8 will give 0x1000
        offset_from_creator = element.tag.element - (create_tag_element << 8)

        return {"creator": {"tagGroup": tag_group, "creatorName": create_dataset.value},
                "element": {"element": element, "offset": offset_from_creator}}


def is_dicom_file(filePath):
    """
    Check if input file is a DICOM File.
    Args:
        filePath: Path to the file to check. Assume that the file exists.
    Returns:
        True if input file is a DICOM File. False otherwise.
    Raises:
        IOError: If input file does not exist.
    """
    tempFile = open(filePath, 'rb')
    try:
        tempFile.seek(0x80, os.SEEK_SET)
        return tempFile.read(4) == b'DICM'
    except IOError:
        return False
    finally:
        tempFile.close()
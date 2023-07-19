import pydicom

from src import format_tag
from src.actions import initialize_actions
from src.utils import get_private_tag


def anonymize_dataset(dataset: pydicom.Dataset,
                      extra_anonymization_rules: dict = None,
                      delete_private_tags: bool = True) -> None:
    """
    Anonymize a pydicom Dataset by using anonymization rules which links an action to a tag
    Args:
        dataset: pydicom Dataset to anonymize
        extra_anonymization_rules: Rules to be applied on the dataset
        delete_private_tags: If True, private tags will be deleted
    Reutrn:
        None
    """
    actions: dict = initialize_actions()
    if extra_anonymization_rules is not None:
        actions.update(extra_anonymization_rules)

    private_tags = []

    for tag, action in actions.items():

        element = None

        def _range_callback(dataset, data_element):
            """
            Callback function for walk function
            """
            if data_element.tag.group & tag[2] == tag[0] and data_element.tag.element & tag[3] == tag[1]:
                action(dataset, (data_element.tag.group, data_element.tag.element))

        # We are in a repeating group
        if len(tag) > 2:
            dataset.walk(_range_callback)
        # Individual Tags
        else:
            # From : https://github.com/KitwareMedical/dicom-anonymizer/pull/18
            # The meta header information is located in the `file_meta` dataset
            # For tags with tag group `0x0002` we thus apply the action to the `file_meta` dataset
            if tag[0] == 0x0002:
                # Apply rule to meta information header
                action(dataset.file_meta, tag)
            else:
                action(dataset, tag)
            print(tag)
            try:
                element = dataset.get(tag)
            except:
                print("Cannot get element from tag: ", format_tag.tag_to_hex_strings(tag))

            # Get private tag to restore it later
            if element and element.tag.is_private:
                private_tags.append(get_private_tag(dataset, tag))

    # X - Private tags = (0xgggg, 0xeeee) where 0xgggg is odd
    if delete_private_tags:
        dataset.remove_private_tags()

        # Adding back private tags if specified in dictionary
        for privateTag in private_tags:
            creator = privateTag["creator"]
            element = privateTag["element"]
            block = dataset.private_block(creator["tagGroup"], creator["creatorName"], create=True)
            if element is not None:
                block.add_new(element["offset"], element["element"].VR, element["element"].value)


def anonymize_dicom_file(in_file: str, out_file: str,
                         extra_anonymization_rules: dict = None,
                         delete_private_tags: bool = True) -> None:
    """
    Anonymize a DICOM file by modifying personal tags
    Conforms to DICOM standard except for customer specificities.
    Args:
        in_file: input DICOM file. Assume that the file exists.
        out_file: output DICOM file
        extra_anonymization_rules: extra anonymization rules to be applied
        delete_private_tags: define if private tags should be delete or not
    Returns:
        None
    Raises:
        IOError: If input file does not exist or output file cannot be written.
    """
    try:
        dataset = pydicom.dcmread(in_file)
    except IOError:
        raise IOError("Input file does not exist.")

    # Apply extra anonymization rules
    anonymize_dataset(dataset, extra_anonymization_rules, delete_private_tags)

    # Store modified image
    try:
        dataset.save_as(out_file)
    except IOError:
        raise IOError("Output file cannot be written.")
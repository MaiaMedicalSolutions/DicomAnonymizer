from typing import Dict, Callable

import pydicom

from src.dicomfields import *

dictionary = {}


# Default anonymization functions

def get_uid(old_uid: str) -> str:
    """
    Lookup new UID in cached dictionary or create new one if none found
    Args:
        old_uid: UID to be replaced
    Returns:
        new_uid: new UID
    """
    from pydicom.uid import generate_uid
    if old_uid not in dictionary:
        dictionary[old_uid] = generate_uid(None)
    return dictionary.get(old_uid)


def replace_element_uid(element):
    """
    Replace UID(s) with random UID(s)
    The replaced value is kept in a dictionary link to the initial element.value in order to automatically
    apply the same replaced value if we have another UID with the same value
    Args:
        element: pydicom.dataelem.DataElement
    Returns:
        None
    """
    from pydicom.multival import MultiValue
    if type(element.value) == MultiValue:
        # Example of multi-value UID situation: IrradiationEventUID, (0008,3010)
        for k, v in enumerate(element.value):
            element.value[k] = get_uid(v)
    else:
        element.value = get_uid(element.value)


def replace_date_time_element(element):
    """
    Handle the anonymization of date and time related elements.
    Date and time elements are all handled in the same way, whether they are emptied or removed.
    """
    if element.VR == 'DA':
        replace_element_date(element)
    elif element.VR == 'DT':
        replace_element_date_time(element)
    elif element.VR == 'TM':
        replace_element_time(element)


def replace_element_date(element):
    """
    Replace date element's value with '00010101'
    Args:
        element: pydicom.dataelem.DataElement
    Returns:
        None
    """
    element.value = '00010101'


def replace_element_date_time(element):
    """
    Replace date time element's value with '00010101010101.000000+0000'
    Args:
        element: pydicom.dataelem.DataElement
    Returns:
        None
    """
    element.value = '00010101010101.000000+0000'


def replace_element_time(element):
    """
    Replace time element's value with '000000.00'
    Args:
        element: pydicom.dataelem.DataElement
    Returns:
        None
    """
    element.value = '000000.00'


def replace_element(element):
    """
    Replace element's value according to its VR:
    - LO, LT, SH, PN, CS, ST, UT: replace with 'Anonymized'
    - UI: cf replace_element_UID
    - DS and IS: value will be replaced by '0'
    - FD, FL, SS, US, SL, UL: value will be replaced by 0
    - DA: value will be replaced by '00010101'
    - DT: value will be replaced by '00010101010101.000000+0000'
    - TM: value will be replaced by '000000.00'
    - UN: value will be replaced by b'Anonymized' (binary string)
    - SQ: call replace_element for all sub elements
    See https://laurelbridge.com/pdf/Dicom-Anonymization-Conformance-Statement.pdf
    Args:
        element: pydicom.dataelem.DataElement
    Returns:
        None
    Raises:
        NotImplementedError: if VR is not implemented
    """
    if element.VR in ('LO', 'LT', 'SH', 'PN', 'CS', 'ST', 'UT'):
        element.value = 'Anonymized'
    elif element.VR == 'UI':
        replace_element_uid(element)
    elif element.VR in ('DS', 'IS'):
        element.value = '0'
    elif element.VR in ('FD', 'FL', 'SS', 'US', 'SL', 'UL'):
        element.value = 0
    elif element.VR in ('DT', 'DA', 'TM'):
        replace_date_time_element(element)
    elif element.VR == 'UN':
        element.value = b'Anonymized'
    elif element.VR == 'SQ':
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                replace_element(sub_element)
    else:
        raise NotImplementedError('Not anonymized. VR {} not yet implemented.'.format(element.VR))


def replace(dataset, tag):
    """
    D - replace with a non-zero length value that may be a dummy value and consistent with the
    VR
    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None

    """
    element = dataset.get(tag)
    if element is not None:
        replace_element(element)


def empty_element(element):
    """
    Clean element according to the element's VR:
    - SH, PN, UI, LO, LT, CS, AS, ST and UT: value will be set to ''
    - DA: value will be replaced by '00010101'
    - DT: value will be replaced by '00010101010101.000000+0000'
    - TM: value will be replaced by '000000.00'
    - UL, FL, FD, SL, SS and US: value will be replaced by 0
    - DS and IS: value will be replaced by '0'
    - UN: value will be replaced by: b'' (binary string)
    - SQ: all subelement will be called with "empty_element"
    Date and time related VRs are not emptied by replacing their values with a empty string to keep
    the consistency with some software who expect a non null value for those VRs.
    See: https://laurelbridge.com/pdf/Dicom-Anonymization-Conformance-Statement.pdf
    Args:
        element: pydicom.dataelem.DataElement
    Returns:
        None
    Raises:
        NotImplementedError: if VR is not implemented
    """
    if element.VR in ('SH', 'PN', 'UI', 'LO', 'LT', 'CS', 'AS', 'ST', 'UT'):
        element.value = ''
    elif element.VR in ('DT', 'DA', 'TM'):
        replace_date_time_element(element)
    elif element.VR in ('UL', 'FL', 'FD', 'SL', 'SS', 'US'):
        element.value = 0
    elif element.VR in ('DS', 'IS'):
        element.value == '0'
    elif element.VR == 'UN':
        element.value = b''
    elif element.VR == 'SQ':
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                empty_element(sub_element)
    else:
        raise NotImplementedError('Not anonymized. VR {} not yet implemented.'.format(element.VR))


def empty(dataset, tag):
    """
    Z - replace with a zero length value, or a non-zero length value that may be a dummy value and
    consistent with the VR
    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    element = dataset.get(tag)
    if element is not None:
        empty_element(element)


def delete_element(dataset, element):
    """
    Delete the element from the dataset.
    If VR's element is a date, then it will be replaced by 00010101
    Args:
        dataset: pydicom.dataset.FileDataset
        element: pydicom.dataelem.DataElement
    Returns:
        None
    """
    if element.VR == 'DA':
        replace_element_date(element)
    elif element.VR == 'SQ' and isinstance(element.value, pydicom.Sequence):
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                delete_element(sub_dataset, sub_element)
    else:
        del dataset[element.tag]


def delete(dataset, tag):
    """X - remove
    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    element = dataset.get(tag)
    if element is not None:
        delete_element(dataset, element)  # element.tag is not the same type as tag.


def keep(dataset, tag):
    """K - keep (unchanged for non-sequence attributes, cleaned for sequences)
    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    pass


def clean(dataset, tag):
    """
    C - clean, that is replace with values of similar meaning known not to contain identifying
    information and consistent with the VR

    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    Raises:
        NotImplementedError: if VR is not implemented
    """
    if dataset.get(tag) is not None:
        raise NotImplementedError('Tag not anonymized. Not yet implemented.')


def replace_UID(dataset, tag):
    """
    U - replace with a non-zero length UID that is internally consistent within a set of Instances
    Lazy solution : Replace with empty string
    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    element = dataset.get(tag)
    if element is not None:
        replace_element_uid(element)


def empty_or_replace(dataset, tag):
    """Z/D - Z unless D is required to maintain IOD conformance (Type 2 versus Type 1)
    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    replace(dataset, tag)


def delete_or_empty(dataset, tag):
    """X/Z - X unless Z is required to maintain IOD conformance (Type 3 versus Type 2)

    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    empty(dataset, tag)


def delete_or_replace(dataset, tag):
    """X/D - X unless D is required to maintain IOD conformance (Type 3 versus Type 1)

    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    replace(dataset, tag)


def delete_or_empty_or_replace(dataset, tag):
    """
    X/Z/D - X unless Z or D is required to maintain IOD conformance (Type 3 versus Type 2 versus
    Type 1)

    Args:
        dataset: pydicom.dataset.FileDataset
        tag: pydicom.tag.BaseTag
    Returns:
        None
    """
    replace(dataset, tag)


def delete_or_empty_or_replace_UID(dataset, tag):
    """
    X/Z/U* - X unless Z or replacement of contained instance UIDs (U) is required to maintain IOD
    conformance (Type 3 versus Type 2 versus Type 1 sequences containing UID references)
    """
    element = dataset.get(tag)
    if element is not None:
        if element.VR == 'UI':
            replace_element_uid(element)
        else:
            empty_element(element)


def generate_actions(tag_list: list, action: str or Callable, options: dict = None) -> Dict[str, Callable]:
    """
    Generate a dictionary using list values as tag and assign the same value to all
    Args:
        tag_list (list): list of tags
        action (str or Callable): action to apply to the tags
        options (dict): options to pass to the action
    Returns:
        dict: dictionary of actions
    """
    final_action = action
    if not callable(action):
        final_action: Callable = actions_map_name_functions[action] if action in actions_map_name_functions else \
            actions_map_name_functions["keep"]
    if options is not None:
        final_action = final_action(options)
    return {tag: final_action for tag in tag_list}


def initialize_actions() -> Dict[str, Callable]:
    """
    Initialize anonymization actions with DICOM standard values
    Returns:
        dict: dictionary of anonymization actions
    """
    anonymization_actions: Dict[str, Callable] = generate_actions(D_TAGS, actions_map_name_functions["replace"])
    anonymization_actions.update(generate_actions(Z_TAGS, actions_map_name_functions["empty"]))
    anonymization_actions.update(generate_actions(X_TAGS, actions_map_name_functions["delete"]))
    anonymization_actions.update(generate_actions(U_TAGS, actions_map_name_functions["replace_UID"]))
    anonymization_actions.update(generate_actions(Z_D_TAGS, actions_map_name_functions["empty_or_replace"]))
    anonymization_actions.update(generate_actions(X_Z_TAGS, actions_map_name_functions["delete_or_empty"]))
    anonymization_actions.update(generate_actions(X_D_TAGS, actions_map_name_functions["delete_or_replace"]))
    anonymization_actions.update(generate_actions(X_Z_D_TAGS, actions_map_name_functions["delete_or_empty_or_replace"]))
    anonymization_actions.update(
        generate_actions(X_Z_U_STAR_TAGS, actions_map_name_functions["delete_or_empty_or_replace_UID"]))
    return anonymization_actions


actions_map_name_functions = {
    "replace": replace,
    "empty": empty,
    "delete": delete,
    "replace_UID": replace_UID,
    "empty_or_replace": empty_or_replace,
    "delete_or_empty": delete_or_empty,
    "delete_or_replace": delete_or_replace,
    "delete_or_empty_or_replace": delete_or_empty_or_replace,
    "delete_or_empty_or_replace_UID": delete_or_empty_or_replace_UID,
    "keep": keep
}

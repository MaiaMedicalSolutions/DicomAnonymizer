import argparse
import json
import os

import tqdm

from src.anonymizer import anonymize_dicom_file
from src.utils import is_dicom_file

parser = argparse.ArgumentParser(description='Anonymize DICOM files')
parser.add_argument('input_path', type=str, help='Path to the file or folder to anonymize')
parser.add_argument('output_path', type=str, help='Path to the output file or folder')
parser.add_argument('--anonymization_actions', type=str, default=None, help='Path to the anonymization actions file')
parser.add_argument('--keepPrivateTags', type=bool, default=True, help='Define if private tags should be kept or not')
args = parser.parse_args()


def anonymize(input_path: str, output_path: str, anonymization_actions: dict, deletePrivateTags: bool) -> None:
    """
    Read data from input path (folder or file) and launch the anonymization.
    Args:
        input_path: Path to the file or folder to anonymize
        output_path: Path to the output file or folder
        anonymization_actions: Dictionary of anonymization actions
        deletePrivateTags: Define if private tags should be delete or not
    Returns:
        None
    Raises:
        ValueError: If output folder is not set
    """
    # Get input arguments
    input_folder = ''
    output_folder = ''

    if os.path.isdir(input_path):
        input_folder = input_path

    if os.path.isdir(output_path):
        output_folder = output_path
        if input_folder == '':
            output_path = os.path.join(output_folder, os.path.basename(input_path))

    if input_folder != '' and output_folder == '':
        raise ValueError('Error, please set a correct output folder path')

    # Generate list of input file if a folder has been set
    input_files_list = []
    output_files_list = []
    if input_folder == '':
        input_files_list.append(input_path)
        output_files_list.append(output_path)
    else:
        files = os.listdir(input_folder)
        for fileName in files:
            input_file_path = os.path.join(input_folder, fileName)
            output_file_path = os.path.join(output_folder, fileName)
            if is_dicom_file(input_file_path):
                input_files_list.append(input_file_path)
                output_files_list.append(output_file_path)

    progress_bar = tqdm.tqdm(total=len(input_files_list))
    for idx, input_file_path in enumerate(input_files_list):
        anonymize_dicom_file(input_file_path, output_files_list[idx], anonymization_actions, deletePrivateTags)
        progress_bar.update(1)

    progress_bar.close()


if __name__ == "__main__":
    input_path = args.input_path
    output_path = args.output_path
    anonymization_actions = args.anonymization_actions
    keepPrivateTags = args.keepPrivateTags

    if anonymization_actions is None:
        anonymization_actions = {}
    else:
        anonymization_actions = json.loads(anonymization_actions)

    anonymize(input_path, output_path, anonymization_actions, not keepPrivateTags)

import argparse
import json
import os

import tqdm


parser = argparse.ArgumentParser(description='Anonymize DICOM files')
parser.add_argument('input_path', type=str, help='Path to the file or folder to anonymize')
parser.add_argument('output_path', type=str, help='Path to the output file or folder')
parser.add_argument('--anonymization_actions', type=str, default=None, help='Path to the anonymization actions file')
parser.add_argument('--keepPrivateTags', type=bool, default=True, help='Define if private tags should be kept or not')
args = parser.parse_args()


def anonymize(input_path: str, output_path: str, anonymization_actions: dict, deletePrivateTags: bool) -> None:
    pass

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

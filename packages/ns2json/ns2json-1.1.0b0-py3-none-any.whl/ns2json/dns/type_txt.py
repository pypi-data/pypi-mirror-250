"""A module contains functions for extract and format a type TXT data.

"""

import re


def extract_type_txt(data: list) -> list:
    """Extract a type TXT data from a clean data.

    Args:
        data (list): A clean data from the clean_stdout function.

    Returns:
        list: A list contains a extracted data.
        
    """

    type_txt_data = []
    prefix = 'Server:|Address:|Non-authoritative answer:'
    regexp_prefix = '^' + prefix + '.*'
    for value in data:
        if not re.match(regexp_prefix, value):
            type_txt_data.append(value)

    return type_txt_data


def set_type_txt(result: dict, data: list):
    """Set a type TXT data to result variable.

    Args:
        result (dict): A main variable contains final data.
        data (list): Final data from the extract_type_txt function.

    """

    numbers_of_items = len(data)
    match numbers_of_items:
        case 0:
            return  # a default value assigned to the result for TXT type.
        case 1:
            result['types']['txt'] = data[0]
        case _:
            result['types']['txt'] = data

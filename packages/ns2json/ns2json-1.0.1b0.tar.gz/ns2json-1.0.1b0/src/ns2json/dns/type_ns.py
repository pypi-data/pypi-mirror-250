"""A module contains functions for extract and format a type NS data.

"""

import re


def extract_type_ns(data: list, address: str) -> list:
    """Extract a type NS data from a clean data.

    Args:
        data (list): A clean data from the clean_stdout function.
        address (str): A domain name.

    Returns:
        list: A list contains a extracted data.
        
    """

    type_mx_data = []
    for item in data:
        regexp_domain_name = '^www.|^' + address + '.*'
        if re.match(regexp_domain_name, item):
            type_mx_data.append(item)

    formated_type_ns_data = []
    for item in type_mx_data:
        temp_item_splited = item.split('=')
        formated_type_ns_data.append(temp_item_splited[-1])

    return formated_type_ns_data


def set_type_ns(result: dict, data: list):
    """Set a type NS data to result variable.

    Args:
        result (dict): A main variable contains final data.
        data (list): Final data from the extract_type_ns function.

    """

    numbers_of_items = len(data)
    match numbers_of_items:
        case 0:
            return  # a default value assigned to the result for NS type.
        case 1:
            result['types']['ns'] = data[0]
        case _:
            result['types']['ns'] = data

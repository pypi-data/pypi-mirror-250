"""A module contains functions for extract and format a type SOA data.

"""

import re


def extract_type_soa(data: list) -> list:
    """Extract a type SOA data from a clean data.

    Args:
        data (list): A clean data from the clean_stdout function.

    Returns:
        list: A list contains a extracted data.

    """

    type_soa_data = []
    properties = 'primary|responsible|serial|refresh|retry|expire|default'
    regexp_soa_properties = '^' + properties + '.*'
    for item in data:
        if re.match(regexp_soa_properties, item):
            type_soa_data.append(item)

    formated_type_soa_data = []
    for item in type_soa_data:
        temp_item_splited = item.split('=')
        key = temp_item_splited[0]
        regexp_value = '\\(.*\\)'
        value = re.sub(regexp_value, '', temp_item_splited[-1])
        formated_type_soa_data.append([key, value])

    return formated_type_soa_data


def set_type_soa(result: dict, data: list):
    """Set a type SOA data to result variable.

    Args:
        result (dict): A main variable contains final data.
        data (list): Final data from the extract_type_soa function.
        
    """

    numbers_of_items = len(data)
    if numbers_of_items == 0:
        return  # a default value assigned to the result for SOA type.
    else:
        result['types']['soa'] = {}
        for item in data:
            key = item[0]
            value = item[-1]
            result['types']['soa'][key] = value

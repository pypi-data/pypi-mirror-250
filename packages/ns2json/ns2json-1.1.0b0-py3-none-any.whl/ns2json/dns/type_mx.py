"""A module contains functions for extract and format a type MX data.

"""

import re


def extract_type_mx(data: list, address: str) -> list:
    """Extract a type MX data from a clean data.

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

    formated_type_mx_data = []
    for item in type_mx_data:
        temp_item_splited = item.split('=')
        preference = temp_item_splited[1][:temp_item_splited[1].index('m')]
        mailexchanger = temp_item_splited[-1]
        formated_type_mx_data.append([preference, mailexchanger])

    return formated_type_mx_data


def set_type_mx(result: dict, data: list):
    """Set a type MX data to result variable.

    Args:
        result (dict): A main variable contains final data.
        data (list): Final data from the extract_type_mx function.

    """

    numbers_of_items = len(data)
    match numbers_of_items:
        case 0:
            return  # a default value assigned to the result for MX type.
        case 1:
            result['types']['mx'] = {}
            result['types']['mx']['preference'] = data[0][0]
            result['types']['mx']['mailexchanger'] = data[0][1]
        case _:
            result['types']['mx']= {}
            for i in range(len(data)):
                result['types']['mx'][str(i)] = {}
                result['types']['mx'][str(i)]['preference'] = data[i][0]
                result['types']['mx'][str(i)]['mailexchanger'] = data[i][1]

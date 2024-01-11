"""A module contains functions for extract and format a type A data.

"""

import re


def extract_type_a(data: list, dns_resolver: str) -> list:
    """Extract a type A data from a clean data.

    Args:
        data (list): A clean data from the clean_stdout function.
        dns_resolver (str): A DNS Resolver an IPv4 address.

    Returns:
        list: A list contains a extracted data.

    """

    type_a_data = []
    for item in data:
        regexp_dns_resolver = '.*' + dns_resolver +'$'
        regexp_type_a = '.*([0-9]{1,3}[.]){3}[0-9]{1,3}'
        if re.match(regexp_dns_resolver, item):
            continue
        if re.match(regexp_type_a, item):
            type_a_data.append(item)

    formated_type_a_data = []
    for item in type_a_data:
        regexp_prefix = '^Addresses:|Address:'
        if re.match(regexp_prefix, item):
            formated_type_a_data.append(re.sub(regexp_prefix, '', item))
        else:
            formated_type_a_data.append(item)
            
    return formated_type_a_data


def set_type_a(result: dict, data: list) -> None:
    """Set a type A data to result variable.

    Args:
        result (dict): A main variable contains final data
        data (list): Final data from the extract_type_a function.
        
    """

    numbers_of_items = len(data)
    match numbers_of_items:
        case 0:
            return  # a default value assigned to the result for A type.
        case 1:
            result['types']['a'] = data[0]
        case _:
            result['types']['a'] = data

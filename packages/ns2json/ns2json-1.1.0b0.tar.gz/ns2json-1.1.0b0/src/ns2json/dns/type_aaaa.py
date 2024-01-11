"""A module contains functions for extract and format a type AAAA data.

"""

import re


def extract_type_aaaa(data: list, dns_resolver: str) -> list:
    """Extract a type AAAA data from a clean data.

    Args:
        data (list): A clean data from the clean_stdout function.
        dns_resolver (str): A DNS Resolver an IPv4 address.

    Returns:
        list: A list contains a extracted data.

    """

    type_aaaa_data = []
    for item in data:
        regexp_dns_resolver = '.*' + dns_resolver
        regexp_type_aaaa = '.*[0-9a-f]{1,4}:{1,2}.*:[0-9a-f]{1,4}$'
        if re.match(regexp_dns_resolver, item):
           continue
        if re.match(regexp_type_aaaa, item):
            type_aaaa_data.append(item)

    formated_type_aaaa_data = []
    for item in type_aaaa_data:
        regexp_prefix = '^Addresses:|Address:'
        if re.match(regexp_prefix, item):
            formated_type_aaaa_data.append(re.sub(
                regexp_prefix, '', item))
        else:
            formated_type_aaaa_data.append(item)

    return formated_type_aaaa_data


def set_type_aaaa(result: dict, data: list):
    """Set a type AAAA data to result variable.

    Args:
        result (dict): A main variable contains final data
        data (list): Final data from the extract_type_aaaa function.
        
    """

    numbers_of_items = len(data)
    match numbers_of_items:
        case 0:
            return  # a default value assigned to the result for AAAA type.
        case 1:
            result['types']['aaaa'] = data[0]
        case _:
            result['types']['aaaa'] = data

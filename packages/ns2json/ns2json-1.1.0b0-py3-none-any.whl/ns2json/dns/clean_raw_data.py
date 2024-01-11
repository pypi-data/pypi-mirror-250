"""A module contains functions for clean a raw data from the nslookup.

"""

import re


def clean_stdout(data: str) -> list:
    """Clean a raw data from the nslookup.

    Args:
        data (str): A raw data from the nslookup.

    Returns:
        list: A list contains a clean data.
    """

    data_no_tabs = re.sub('\t+', ' ', data)
    data_no_multiple_new_lines = re.sub('\n+', '\n', data_no_tabs)
    data_no_new_line_on_end = re.sub('\n$', '', data_no_multiple_new_lines)
    data_no_multiple_spaces = re.sub(' +', '', data_no_new_line_on_end)
    data_no_extra_characters = re.sub('[\',]', '', data_no_multiple_spaces)
    clean_splited_data = data_no_extra_characters.split('\n')

    return clean_splited_data


def clean_stdout_for_type_txt(data: str, address: str) -> list:
    """Clean a raw data for the type TXT from the nslookup.

    Args:
        data (list): A raw data from the nslookup.
        address (str): A domain name.

    Returns:
        list: A list contains a clean data.
    """

    data_no_multiple_new_lines = re.sub('\n+', '\n', data)
    data_no_multiple_tabs = re.sub('\t+', '', data_no_multiple_new_lines)
    data_no_multiple_spaces = re.sub(' {2,}', '', data_no_multiple_tabs)
    data_no_new_line_on_end = re.sub('^\n|\n$', '', data_no_multiple_spaces)
    regexp_special_characters = address + 'text =\n'
    data_no_extra_characters = re.sub(
        regexp_special_characters, '', data_no_new_line_on_end)
    clean_splited_data = data_no_extra_characters.split('\n')
    final_clean_data = []
    for i in clean_splited_data:
        final_clean_data.append(re.sub('^"|"$', '', i))

    return final_clean_data

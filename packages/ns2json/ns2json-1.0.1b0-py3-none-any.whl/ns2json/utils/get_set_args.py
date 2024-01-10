"""A module contains functions for set and get data from a user.

"""

import os
import sys
import re


def format_domain_name(domain: str) -> str:
    """Remove http, https, www, and subpages from an address.

    Args:
        domain (str): A domain name from a user.

    Returns:
        str: Formated a domain name.

    """

    regexp_remove_prefix = '^http://|https://|www.'
    no_domain_prefix = re.sub(regexp_remove_prefix, '', domain)
    regexp_remove_sufix = '/.*'
    final_domain = re.sub(regexp_remove_sufix, '', no_domain_prefix)
    return final_domain


def check_args_type() -> dict:
    """Find with one from cli arguments are an address, a DNS resolver, and a path.

    Returns:
        dict: A variable contains an addressm a DNS resolver, and a path.

    """    

    final_args = {
        'address': '',
        'dns_resolver': '',
        'path': ''
    }
    regexp_address = '^(https://)|(http://)|(www.)|(.*[.])'
    regexp_dns_resolver = '^([0-9]{1,3}.){1,3}[0-9]{1,3}$'
    regexp_path = r'^.*\\{1,2}.*'

    is_address_set = False
    is_dns_resolver_set = False
    is_path_set = False
    for arg in sys.argv[1:]:
        if re.match(regexp_dns_resolver, arg) and not is_dns_resolver_set:
            final_args['dns_resolver'] = arg
            is_dns_resolver_set = True
        elif re.match(regexp_address, arg) and not is_address_set:
            final_args['address'] = format_domain_name(arg)
            is_address_set = True
        elif re.match(regexp_path, arg) and not is_path_set:
            final_args['path'] = arg
            is_path_set = True
    return final_args


def get_args_from_cli_line() -> dict:
    """Extract data putted by a CLI from a user.

    Raises:
        Exception: Too small or too high number or arguments.

    Returns:
        dict: Final data contains a domain name, a DNS resolver address, and a path to save an JSON file.

    """

    numbers_of_args = len(sys.argv)
    if not 1 < numbers_of_args < 5:
        raise Exception()
    
    final_args = check_args_type()
    if final_args['address'] == '':
        raise Exception()
    if final_args['dns_resolver'] == '':
        final_args['dns_resolver'] = '1.1.1.1'
    if final_args['path'] == '':
        final_args['path'] = os.getcwd()
    return final_args


def set_args_from_cli_to_result(result: dict, final_args: dict) -> str:
    """Insert a domain name, and a DNS resolver address to a resoult variable.

    Args:
        result (dict): A main variable contains final data.
        args (dict): A dictionary contains a domain name, a DNS resolver, and path to save a JSON file. 

    Returns:
        str: A path to save a JSON file.

    """

    result['address'] = final_args['address']
    result['dns_resolver'] = final_args['dns_resolver']
    return final_args['path']

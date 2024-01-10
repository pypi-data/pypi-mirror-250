"""Executable the NS2JSON script file. The script pulls data from a DNS resolver and exports it to a JSON file. The file contains type A, AAAA, MX, NS, SOA, TXT informations.

"""

import sys
from .utils.get_set_args import get_args_from_cli_line, set_args_from_cli_to_result
from .utils.export_data import export_result_to_json
from .dns.pull_data import pull_data_from_dns
from .dns.format_data import format_data_from_dns


def main() -> None:
    """A main script function.

    """ 

    dns_types = ['a', 'aaaa', 'mx', 'ns', 'soa', 'txt']
    path_to_save_json = 'None'
    raw_stdout = {
        'a': 'None',
        'aaaa': 'None',
        'mx': 'None',
        'ns': 'None',
        'soa': 'None',
        'txt': 'None',
    }
    # A main variable contains all data to export to a JSON file.
    result = {
        'address': 'None',
        'dns_resolver': 'None',
        'types': {
            'a': 'None',
            'aaaa': 'None',
            'mx': 'None',
            'ns': 'None',
            'soa': 'None',
            'txt': 'None',
        },
    }

    try:
        path_to_save_json = set_args_from_cli_to_result(
            result, get_args_from_cli_line())
    except:
        print('Error: The script needs a minimum of one argument: a domain name. But you can put a maximum of three in order: a domain name, a DNS resolver address, and a path to save a JSON file.')
        sys.exit(1)
    
    try:
        pull_data_from_dns(result, raw_stdout, dns_types)
    except:
        print('Error: A problem with communication with the DNS resolver. Cannot pull data from a server.')
        sys.exit(1)

    try:
        format_data_from_dns(result, raw_stdout, dns_types)
    except:
        print('Something was wrong with the data format process.')
        sys.exit(1)

    try:
        export_result_to_json(result, path_to_save_json)
    except:
        print('Error: Cannot save the JSON file in a currently path.')
        sys.exit(1)

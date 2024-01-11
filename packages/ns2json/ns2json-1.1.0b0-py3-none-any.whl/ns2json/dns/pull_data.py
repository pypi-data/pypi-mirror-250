"""A module contains function for pull a data from a DNS resolvers.

"""

import subprocess


def pull_data_from_dns(result: dict, raw_stdout: dict, dns_types: list) -> None:
    """Ask a DNS resolver about types and save a raw data.

    Args:
        result (dict): A final variable constains data to export.
        raw_stdout (dict): A variable to save raw data from a DNS resolver.
        dns_types (list): A list contains DNS types to ask.

    """

    for dns_type in dns_types:
        raw_stdout[dns_type] = subprocess.run(
            ['nslookup', '-type=' + dns_type, result['address'], result['dns_resolver']], timeout=1, check=True, capture_output=True, encoding='utf-8').stdout

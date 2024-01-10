"""A module contains functions to clean, extract and set data to the final variable.

"""

from .clean_raw_data import clean_stdout, clean_stdout_for_type_txt
from .type_a import extract_type_a, set_type_a
from .type_aaaa import extract_type_aaaa, set_type_aaaa
from .type_mx import extract_type_mx, set_type_mx
from .type_ns import extract_type_ns, set_type_ns
from .type_soa import extract_type_soa, set_type_soa
from .type_txt import extract_type_txt, set_type_txt


def format_data_from_dns(result: dict, raw_stdout: dict, dns_types: list) -> None:
    """Clean, extract and set data from raw data delivered by DNS resolver.

    Args:
        result (dict): A final variable constains data to export.
        raw_stdout (dict): A variable to save raw data from a DNS resolver.
        dns_types (list): A list contains DNS types to ask.

    """

    for dns_type in dns_types:
        match dns_type:
            case 'a' | 'aaaa' | 'mx' | 'ns' | 'soa':
                clean_data = clean_stdout(raw_stdout[dns_type])
            case 'txt':
                clean_data = clean_stdout_for_type_txt(
                    raw_stdout[dns_type], result['address'])
        match dns_type:
            case 'a':
                set_type_a(result, extract_type_a(
                    clean_data, result['dns_resolver']))
            case 'aaaa':
                set_type_aaaa(result, extract_type_aaaa(
                    clean_data, result['dns_resolver']))
            case 'mx':
                set_type_mx(result, extract_type_mx(
                    clean_data, result['address']))
            case 'ns':
                set_type_ns(result, extract_type_ns(
                    clean_data, result['address']))
            case 'soa':
                set_type_soa(result, extract_type_soa(clean_data))
            case 'txt':
                set_type_txt(result, extract_type_txt(clean_data))

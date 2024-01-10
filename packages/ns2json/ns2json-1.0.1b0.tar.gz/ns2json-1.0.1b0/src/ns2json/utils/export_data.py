"""A Module contains function to export filan data to a JSON file.

"""

import json


def export_result_to_json(result: dict, path_to_save_json: str) -> None:
    """Export final data to a JSON file.

    Args:
        result (dict): A final variable constains data to export.
        path_to_save_json (str): A path to save a JSON file.

    """

    result_json_format = json.dumps(result)
    file_name = result['address'] + '.json'
    file = open(path_to_save_json + '\\' + file_name, 'w')
    file.write(result_json_format)
    file.close()

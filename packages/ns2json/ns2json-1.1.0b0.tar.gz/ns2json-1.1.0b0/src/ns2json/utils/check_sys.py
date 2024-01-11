"""A module contains a function to check a user's OS.

"""

import platform


def is_correct_platform() -> None:
    """Check if the script is executing on the correct OS.

    Raises:
        Exception: Return if the OS is not correct.
        
    """

    if not platform.system() == 'Windows':
        raise Exception()

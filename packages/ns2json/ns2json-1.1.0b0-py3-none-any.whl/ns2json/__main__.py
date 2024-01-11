"""A main file to execute the script from CLI by name of package. 

"""

import sys
from .utils.check_sys import is_correct_platform
from .ns2json import main

if __name__ == '__main__':
    try:
        is_correct_platform()
    except:
        print('Error: The script can currently run only on the Windows platform.')
        sys.exit(1)

    sys.exit(main())

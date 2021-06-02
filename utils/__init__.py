import os
import platform
import sys

from appdirs import AppDirs

pluck = lambda dict, *args: (dict[arg] for arg in args)

dirs = AppDirs("SpectographViewer", "SpectographViewer")
print('----------')

# for d in dir(dirs):
#     print('  %s' % d)

print('user_state_dir', dirs.user_state_dir)
print('user_data_dir', dirs.user_data_dir)

_IS_MAC = platform.system() == 'Darwin'


def getRightDirs():
    """Get the DATA_PATH and the resource_dir pathes.
    DATA_PATH is on the user side if CB is frozen"""

    if getattr(sys, "frozen", False):
        # resource_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        resource_dir = sys._MEIPASS
        DATA_PATH = dirs.user_config_dir
    else:
        resource_dir = '.'
        DATA_PATH = '.'

    # Create the user directory if it doesn't exist
    os.makedirs(DATA_PATH, exist_ok=True)

    return resource_dir, DATA_PATH

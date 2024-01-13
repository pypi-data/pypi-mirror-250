"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)

"""

import os


__version__ = '0.2.3'

# Library and resource paths
PATH_LIB = os.path.dirname(__file__) + os.sep
PATH_RES = PATH_LIB + 'resources' + os.sep

# from . import ephem
# ephem.setPath(PATH_RES+'swefiles')
from . import const
const.SE_PATH = PATH_RES+'swefiles'
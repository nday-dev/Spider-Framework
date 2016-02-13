#--coding:utf-8--
"""
Import all things in tmpl
------------
List:
    cfgFile
    Distributor
    Extractor
    Platform
    Prompt
"""

if __name__ == '__main__':
    raise EnvironmentError("DO NOT DIRECTLY RUN THIS SCRIPT!")

import os
import sys
sys.path.append(os.path.pardir)
from tmpl import *
sys.path.pop()


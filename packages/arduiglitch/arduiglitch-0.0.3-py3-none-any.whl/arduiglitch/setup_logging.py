"""
This file contains misc functions to setup the logging system.
The YAML logger config file is the one that refers to the functions in this script.
"""

import logging

# Filter, accessed in yaml logger setup file
class infoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.INFO

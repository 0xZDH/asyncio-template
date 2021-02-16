#!/usr/bin/env python3

# Asyncio Template Commenting:
#   TODO:      Instructions for modifications or updates per tooling.
#   EXAMPLE:   Examples of code blocks that can be leveraged.
#   NOTE:      Details of specific code blocks that can/should be modified
#              per reorganization of code.

# NOTE: This support file is meant to provide easy access to data manipulation
#       functions across all modules that we will need to reuse.

import re
import logging
import requests

# NOTE: This uses the default values from `core/config.py`
from core.config import RAW_FILE, OUT_FILE, HTTP_HEADERS

class Support:
    """ Helper functions """

    # NOTE: The following functions are examples of global support functions
    #       that any module can leverage.

    def __init__(self, out_dir):
        # NOTE: When initializing the support class, we set the output dir
        #       and open a file handle to our log file to write to during
        #       execution. The log file is written to in real-time so we want
        #       to keep a handle open during execution and only close it when
        #       the tool is exiting.
        self.out_dir  = out_dir
        self.log_file = open(f"{out_dir}{RAW_FILE}", 'a')

    def check_email(self, email):
        """ Validate email address syntax """
        # NOTE: This is a super basic example of a validation function to check
        #       the syntax of a given email address across modules.
        return re.fullmatch('[^@]+@[^@]+\.[^@]+', email)

    def write_results(self, results):
        """ Write valid emails to results directory """
        # NOTE: This function is leveraged during the module shutdown functions
        #       in order to write valid results to a specified dir and file.
        if len(results) > 0:
            with open(f"{self.out_dir}{OUT_FILE}", 'a') as out_file:
                for item in results:
                    out_file.write(f"{item}\n")

    def write_logs(self, data):
        """ Write raw responses/data to results directory """
        # NOTE: Basic logging function to write any raw data passed to a
        #       log file we specify.
        self.log_file.write(f"{data}\n")

    def close_logs(self):
        """ Close the log file handle on shutdown """
        # NOTE: Since we open a log file handle, we want to ensure to close it
        #       before the tool quits so this function should be called from a
        #       module's shutdown functions.
        self.log_file.close()

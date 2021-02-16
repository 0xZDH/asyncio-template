#!/usr/bin/env python3

# Asyncio Template Commenting:
#   TODO:      Instructions for modifications or updates per tooling.
#   EXAMPLE:   Examples of code blocks that can be leveraged.
#   NOTE:      Details of specific code blocks that can/should be modified
#              per reorganization of code.

# == Global Settings

# NOTE: File names to write successful results and raw logs to. The
#       output directory where these files are written is initialized
#       within main.py.
RAW_FILE = "raw.log"
OUT_FILE = "successful_results.txt"

# NOTE: Default HTTP Header configuration. When making an HTTP request,
#       a module can add/remove headers as needed by setting up a custom
#       headers variable internal to the class _execute function that can
#       then be passed to the _send_request function.
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) " +
                  "Gecko/20100101 Firefox/69.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

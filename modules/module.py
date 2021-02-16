#!/usr/bin/env python3

# Asyncio Template Commenting:
#   TODO:      Instructions for modifications or updates per tooling.
#   EXAMPLE:   Examples of code blocks that can be leveraged.
#   NOTE:      Details of specific code blocks that can/should be modified
#              per reorganization of code.

# NOTE: This is a template of a module that performs a task such as HTTP
#       requests.

import json
import time
import logging
import urllib3
import asyncio
import requests
import concurrent.futures
import concurrent.futures.thread

from functools import partial
from core.config import *
from core.support import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Module(object):

    # TODO: Modify the URL based on the target task. If not an HTTP module,
    #       remove completely/replace with global, target data.
    TGT_URL  = "https://api.localhost?item={ITEM}"

    # Storage for successful results of each task
    successful_results = []

    def __init__(self, *args, **kwargs):
        # NOTE: Accept multiple kwargs during module initialization to allow for things
        #       like the asyncio loop and command line flags to be provided.
        self.args    = kwargs['args']
        self.loop    = kwargs['loop']
        self.out_dir = kwargs['out_dir']
        self.support = Support(out_dir=self.out_dir)  # Helper functions
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.args.rate
        )
        # NOTE: Proxy is initialized specifically for modules that leverage 'requests'
        #       to perform HTTP request tasks.
        self.proxies = None if not self.args.proxy else {
            "http": self.args.proxy, "https": self.args.proxy
        }

    def shutdown(self, key=False):
        """ Perform a shutdown and clean up of the asynchronous handler """
        # TODO: Define the module shutdown message and functionality
        # EXAMPLE: Writing successful results to a specific output dir
        #
        print()  # Print empty line
        msg = f"Writing successful results to: '{self.out_dir}'"
        if key:
            logging.warning("CTRL-C caught")
        logging.info(msg)

        # NOTE: The following 3 lines of code using 'atexit' should *not be touched*
        #       or modified as this is the handler to remove remaining threads if a
        #       CTRL-C is caught. This is *required*
        # https://stackoverflow.com/a/48351410
        # https://gist.github.com/yeraydiazdiaz/b8c059c6dcfaf3255c65806de39175a7
        # Unregister _python_exit while using asyncio
        # Shutdown ThreadPoolExecutor and do not wait for current work
        import atexit
        atexit.unregister(concurrent.futures.thread._python_exit)
        self.executor.shutdown = lambda wait:None
        # 
        # NOTE: End of *do not touch* code block

        # Write the successful results
        self.support.write_results(self.successful_results)

        # Close out the raw logs file handle
        self.support.close_logs()
        #
        # END EXAMPLE

    def _send_request(self, request, url, auth=None, data=None,
                      json_data=None, headers=HTTP_HEADERS):
        """ Template for HTTP Requests """
        # NOTE: General template of a request function that can accept multiple
        #       variations and data sets.
        return request(url,
                       auth=auth,
                       data=data,
                       json=json_data,
                       headers=headers,
                       proxies=self.proxies,
                       timeout=self.args.timeout,
                       allow_redirects=False,
                       verify=False)

    def _execute(self, item):
        """ Perform an asynchronous task """
        # TODO: This is the 'core' function of the module that will handle the logic for
        #       the task being performed.
        try:
            # NOTE: Add a small sleep before each task is performed in order to allow for
            #       cleaner processing.
            time.sleep(0.250)

            # --------------------------------------------------------
            # For new modules, modify the below code block logic

            # TODO: For HTTP based tasks, manipulate the global target URL with the
            #       given item for this task.
            url = self.TGT_URL.format(ITEM=item)

            # TODO: Perform an HTTP request and collect the results. Pass the HTTP
            #       request type via the first parameter and any subsequent data
            #       required after (url, data, headers, etc.).
            response    = self._send_request(requests.get, url)
            resp_status = response.status_code

            # TODO: If a specific status code is not achieved, do no process the
            #       results.
            if resp_status != 200:
                return

            # TODO: Perform the bulk of the logic here - collect the data needed from the
            #       request's response and process however the task is meant to handle it.

            # EXAMPLE: Grab and parse the HTTP response headers in order to identify if a
            #          given header was set on server response.
            #
            r_headers = response.headers

            # Write the raw data we are parsing to the logs
            self.support.write_logs(r_headers)

            if "target_header" in (c.lower() for c in r_headers.keys()):
                self.successful_results.append(item)
                logging.info(f"[ + ] Valid result: {item}")
            else:
                logging.info(f"[ - ] Invalid result: {item}")
            #
            # END EXAMPLE

            # End template module code block logic.
            # --------------------------------------------------------

        except Exception as e:
            logging.debug(e)
            pass

    async def run(self, items):
        """ Asyncronously execute task(s) """
        # NOTE: Build a list of blocking tasks via run_in_executor which are just
        #       instances of the _execute function with single items to be processed.
        blocking_tasks = [
            self.loop.run_in_executor(self.executor,
                                      partial(self._execute,
                                              item=item))
            for item in items
        ]

        # NOTE: While there are still blocking tasks, await this function.
        if blocking_tasks:
            await asyncio.wait(blocking_tasks)

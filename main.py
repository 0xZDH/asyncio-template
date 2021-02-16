#!/usr/bin/env python3

# Asyncio Template Commenting:
#   TODO:      Instructions for modifications or updates per tooling.
#   EXAMPLE:   Examples of code blocks that can be leveraged.
#   NOTE:      Details of specific code blocks that can/should be modified
#              per reorganization of code.

import os
import sys
import time
import signal
import logging
import asyncio
import argparse
from pathlib import Path

# NOTE: Import all modules via modules/__init__.py
from modules import *

__tool__    = "Asyncio Template"
__version__ = "1.0"
__status__  = "prod"

def signal_handler(signal, frame):
    """ Signal handler for async routines.
        Call the module's shutdown function to cleanly exit upon
        receiving a CTRL-C signal.
    """
    module.shutdown(key=True)
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{__tool__} -- " +
                                                 f"v{__version__}-{__status__}")

    # TODO: Add any arguments required here for data input from the user.
    # EXAMPLE: Mutually exclusive flag group for single, multi, or file
    #          of items to process:
    #
    item_group  = parser.add_mutually_exclusive_group()
    item_group.add_argument("-a", "--argA", type=str,
                            help="Single item to process.")
    item_group.add_argument("-b", "--argB", type=str, nargs='+',
                            help="Multiple items to process.")
    item_group.add_argument("-c", "--argC", type=str,
                            help="File containing multiple items to process.")
    #
    # END EXAMPLE

    # NOTE: --timeout and --proxy are specific flags for tooling that requires the
    #       use of requests (any web based tool).
    parser.add_argument("--timeout", type=int, default=25,
                        help="Request timeout in seconds. Default: 25")
    parser.add_argument("--proxy",   type=str,
                        help="Proxy to pass traffic through " +
                             "(e.g. http://127.0.0.1:8080).")

    # NOTE: Generic tool modification flags.
    parser.add_argument("--rate",    type=int, default=10,
                        help="Number of concurrent connections during " +
                             "verification. Default: 10")
    parser.add_argument("--version", action="store_true",
                        help="Print the tool version.")
    parser.add_argument("--debug",   action="store_true",
                        help="Debug output")

    args = parser.parse_args()

    # Print the tool version and exit
    if args.version:
        print(f"{__tool__} v{__version__}-{__status__}")
        sys.exit(0)

    # Track execution time
    exec_start = time.time()

    # TODO: Logging output for standard vs. debug handling.
    # Initialize logging level and format
    if args.debug:
        logging_format = "[%(asctime)s] %(levelname)-5s - %(filename)20s:%(lineno)-4s " + \
                         "- %(message)s"
        logging_level  = logging.DEBUG
    else:
        logging_format = "[%(asctime)s] %(levelname)-5s: %(message)s"
        logging_level  = logging.INFO

    logging.basicConfig(format=logging_format, level=logging_level)
    # NOTE: Update logging level name of WARNING to enforce consistent lengths
    #       of 5 char or less for better formatting.
    logging.addLevelName(logging.WARNING, "WARN")

    # - Handle flag validations

    # NOTE: To allow for the `--version` flag, we don't want to require
    #       any flags. Instead, we manually validate required flags and
    #       pairings here.
    # EXAMPLES:
    #
    # Require either argA or argB or argC
    if (not args.argA and not args.argB and not args.argC):
        sys.exit(1)

    # Ensure that a file passed is a valid file
    if (args.argC and not os.path.isfile(args.argC)):
        sys.exit(1)
    #
    # END EXAMPLES

    # - Begin enumeration

    # Initialize the Asyncio loop
    loop = asyncio.get_event_loop()

    # Add signal handler to handle ctrl-c interrupts
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # NOTE: Build and initialize the output directory handler to be used
    #       by the modules during shutdown
    NEW_DIR    = "results"
    CUR_DIR    = Path(__file__).parent.absolute()
    OUTPUT_DIR = f"{CUR_DIR}/{NEW_DIR}/"

    # Create output directory (if not already present)
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # TODO: Add conditionals and any extra modules here to initialize
    #       based on the flags provided by the user (if providing flags
    #       that allow the user to specify the module to use).

    # Build the module parameters and initialize the module class
    kwargs = { 'loop': loop, 'args': args, 'out_dir': OUTPUT_DIR }
    module = Module(**kwargs)
    # EXAMPLE: Conditional to handle more than one module based on args
    #
    # if args.moduleA:   module = ModuleA(**kwargs)
    # elif args.moduleB: module = ModuleB(**kwargs)
    #
    # END EXAMPLE

    try:
        # TODO: Update arguments for single item handling. We make the
        #       single item into a list for consistent data handling
        #       within the module.
        # Handle a single item to be processed
        if args.argA:
            loop.run_until_complete(module.run([args.argA]))

        # TODO: Update arguments for multiple item handling. Since the
        #       items are already a list, we can pass them directly to
        #       the module.
        # Handle list of/multiple items to be processed
        elif args.argB:
            loop.run_until_complete(module.run(args.argB))

        # TODO: Update arguments for file/multi-item handling. We first
        #       convert the file lines to a cleaned output and then pass
        #       directly to the module.
        # Handle file of items to be processed
        else:
            with open(args.argC, 'r') as in_file:
                # Clean input
                items = [ item.strip() for item in in_file.readlines() ]
                loop.run_until_complete(module.run(items))

        # NOTE: Call the module's shutdown function to exit cleanly. Otherwise,
        #       it can be triggered via a CTRL-C signal.
        module.shutdown()

        # NOTE: Give the loop a bit more time to ensure all threads are cleaned
        #       up after receiving the shutdown signal.
        loop.run_until_complete(asyncio.sleep(0.250))
        loop.close()
    except KeyboardInterrupt as e:
        pass

    # Display tracked timer
    print()  # Add a new line before final output
    elapsed = time.time() - exec_start
    logging.info(f"{__file__} executed in {elapsed:.2f} seconds.")

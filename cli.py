#!/usr/bin/env python3

__author__ = "Andrew Szymanski ()"
__version__ = "0.1"

""" main script
"""
import sys
import logging
import os
import inspect
import imp
import traceback


LOG_INDENT = "  "
logger = logging.getLogger("adsafds")
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s',"%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logger.addHandler(console)
logger.setLevel(logging.DEBUG)     # default, this will be reset later


def main(argv=None):
    from optparse import OptionParser, OptionGroup
    logger.debug("main starting...")

    argv = argv or sys.argv
    parser = OptionParser(description="python extendable REST client (based on restkit)",
                      version=__version__,
                      usage="usage: %prog [options]")
    # cat options
    cat_options = OptionGroup(parser, "options")
    cat_options.add_option("-d", "--debug", help="debug logging, specify any value to enable debug, omit this param to disable, example: --debug=False", default=False)
    parser.add_option_group(cat_options)

    try: 
        opts, args = parser.parse_args(argv[1:])
    except Exception as e:
        sys.exit("ERROR: [%s]" % e)

    #mainRun(opts, parser)


if __name__ == "__main__":
    logger.info("__main__ starting...")
    try:
        main()
    except Exception as e:
        sys.exit("ERROR: [%s]" % e)    
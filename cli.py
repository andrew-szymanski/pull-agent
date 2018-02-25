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
import fcntl
import time


# globals
LOG_INDENT = "  "
logger = logging.getLogger("polling-deployer")
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s',"%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logger.addHandler(console)
logger.setLevel(logging.DEBUG)     # default, this will be reset later

LOCK_FILE_FULLPATH="/tmp/polling-deployer.lck"
STOP_FILE_FULLPATH="/tmp/polling-deployer.stop"



class Poller(object):
    """ Class for polling functionality
    """
    def __init__(self, **kwargs):
        """Create an object and attach or initialize logger
        """
        self.logger = kwargs.get('logger',None)
        if ( self.logger is None ):
            # Get an instance of a logger
            self.logger = logger
        # initial log entry
        self.logger.setLevel(logger.getEffectiveLevel())
        self.logger.debug("%s: %s version [%s]" % (self.__class__.__name__, inspect.getfile(inspect.currentframe()),__version__))
      

    def run(self, *args, **kwargs):
        """ start singleton logger
        """
        self.logger.debug("%s::%s starting..." %  (self.__class__.__name__ , inspect.stack()[0][3])) 
        self.logger.debug("args: [%s]" % args)
        self.logger.debug("lockfile: [%s]" % LOCK_FILE_FULLPATH)
        #
        lock_file = LOCK_FILE_FULLPATH
        fp = open(lock_file, 'w')
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            # another instance is running
            self.logger.warn("another instance already running - exiting")
            sys.exit(0)
      
        self.logger.info("poller starting...")
        # check if stop file exists and make sure it doesn't
        if os.path.exists(STOP_FILE_FULLPATH):
            self.logger.info("stop file exists on start - removing it")
            os.remove(STOP_FILE_FULLPATH)
        self.poll()

    def stop(self, *args, **kwargs):
        """ stop singleton logger
        """
        self.logger.debug("%s::%s starting..." %  (self.__class__.__name__ , inspect.stack()[0][3])) 
        self.logger.debug("stopfile: [%s]" % STOP_FILE_FULLPATH)
        #
        stop_file = STOP_FILE_FULLPATH
        fp = open(stop_file, 'w')
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            # another instance is running
            self.logger.warn("stop command already issued")
            sys.exit(0)

    def poll(self):
        """ main polling loop
        """
        self.logger.debug("%s::%s starting..." %  (self.__class__.__name__ , inspect.stack()[0][3])) 
        while True:
            time.sleep(2)
            self.logger.debug("going to sleep...")

            # check if stop file exists
            if os.path.exists(STOP_FILE_FULLPATH):
                self.logger.info("request to stop received...")
                os.remove(STOP_FILE_FULLPATH)
                exit(0)



def run_poller_command(command, args):
    logger.info("%s starting..." % inspect.stack()[0][3])
    logger.debug("command: [%s], args: [%s]" % (command, args))

    # switch
    if ( command == 'run' ):
        logger.debug("starting polller...")
        poller = Poller(logger=logger)
        poller.run(args)
        return;

    if ( command == 'stop' ):
        logger.debug("stopping polller...")
        poller = Poller(logger=logger)
        poller.stop(args)
        return;        

    # try:
    #     # execute specified class method
    #     poller.run(logger=logger, args)   
    # except Exception as caughtException:
    #     print "ERROR: [%s]" % (caughtException,'\n')
    #     sys.exit(1)
    

    logger.info("all done")          
 


def run_main(opts, args):
    logger.info("%s starting..." % inspect.stack()[0][3])

    (component, command) = opts.command.split(".")
    if ( component == 'poller' ):
        run_poller_command(command, args)


# commands:
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
    cat_options.add_option("-c", "--command", help="command, see README.md, example: --command=poller.stop", default=False)
    parser.add_option_group(cat_options)

    try: 
        opts, args = parser.parse_args(argv[1:])
    except Exception as e:
        sys.exit("ERROR: [%s]" % e)

    run_main(opts, args)


if __name__ == "__main__":
    logger.info("__main__ starting...")
    try:
        main()
    except Exception as e:
        sys.exit("ERROR: [%s]" % e)    
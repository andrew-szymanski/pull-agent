

import multiprocessing
import time
import os


# worker 



def worker(logger, file_fullpath):
    """worker function"""
    name = multiprocessing.current_process().name
    logger.debug("   [%s] starting, filename: [%s]" % (name, file_fullpath) )
    os.remove(file_fullpath)
    time.sleep(10)
    logger.debug("   [%s] exiting" % name)
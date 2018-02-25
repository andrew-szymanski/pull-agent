

import multiprocessing
import time
import os


# worker 



def worker(logger, file_fullpath):
    """worker function"""
    name = multiprocessing.current_process().name
    logger.info("   [%s] starting, filename: [%s]" % (name, file_fullpath) )
    os.remove(file_fullpath)
    time.sleep(10)
    logger.info("   [%s] exiting" % name)
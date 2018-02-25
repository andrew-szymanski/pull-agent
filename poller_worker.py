

import multiprocessing
import time


# worker 



def worker(logger, filename):
    """worker function"""
    name = multiprocessing.current_process().name
    logger.debug("[%s] starting, filename: [%s]" % (name, filename) )
    time.sleep(2)
    logger.debug("[%s] exiting" % name)
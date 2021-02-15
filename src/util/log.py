import os
import time
import logging


def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


    fh = logging.FileHandler('log.txt')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)

    # sh = logging.StreamHandler()
    # sh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(levelname)s: %(message)s')
    # sh.setFormatter((formatter))

    logger.addHandler(fh)
    # logger.addHandler(sh)
    return logger


LOG = getLogger()

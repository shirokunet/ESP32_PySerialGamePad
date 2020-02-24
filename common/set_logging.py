#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import logging

def set_logging(name, cfg_log_level='info', stream=True, file=False, dir='log/', filetype='.log'):
    logger = logging.getLogger(name)
    if cfg_log_level == 'debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # StreamHandler
    if stream:
        formatter = logging.Formatter('[%(asctime)s] %(module)s.%(funcName)s %(levelname)s -> %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    # FileHandler
    if file:
        formatter = logging.Formatter('%(asctime)s,%(created)s,%(module)s,%(funcName)s,%(levelname)s,%(message)s')
        current_datetime = datetime.datetime.now()
        filename = dir + current_datetime.strftime('20%y%m%d_%H%M_') + name + filetype
        fh = logging.FileHandler(filename, )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
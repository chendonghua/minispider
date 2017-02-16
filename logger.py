# encoding:utf-8
"""
Author: cdhmuer333@126.com
Created time: 16/12/19 15:07
"""

import logging.handlers
import os
from os.path import dirname
from os.path import abspath
from os.path import join

LOG_FILE = join(dirname(abspath(__file__)),
                        'logs' + os.sep + 'spider.log')
VERSION = "1.0.0"

handler = logging.handlers.RotatingFileHandler(LOG_FILE,
                                               maxBytes=100 * 1024 * 1024,
                                               backupCount=10)

logger = logging.getLogger(LOG_FILE)

logger.setLevel(logging.DEBUG)

fmt = '[%(asctime)s]-[%(levelname)s]-[%(processName)s:%(process)s] %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger.addHandler(handler)


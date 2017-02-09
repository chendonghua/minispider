# encoding:utf-8
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: chendonghua@baidu.com
Created time: 17/1/6 11:52
"""

import os
from config_reader import ConfReader

class SeedFileReader(object):
    """
    负责读取种子文件
    """
    def __init__(self,
                 file_name='seeds.txt'):
        cur_file = os.path.abspath(__file__)
        cur_dir = os.path.join(os.path.dirname(cur_file),
                               ConfReader.instance().get_url_list_file())
        self._file_name = os.path.join(cur_dir, file_name) # absolute path

    def read(self):
        """
        :return: 返回文件中的一行
        """
        with open(self._file_name, 'r') as f:
            for each_line in f:
                yield each_line


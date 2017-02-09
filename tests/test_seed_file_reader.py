# encoding:utf-8
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: chendonghua@baidu.com
Created time: 17/1/12 11:59
"""

from seedfile_reader import SeedFileReader
import unittest

class TestSeedFileReader(unittest.TestCase):
    """
    SeedFileReader测试类
    """
    def test_read(self):
        """
        测试种子文件读取
        """
        reader = SeedFileReader('seeds.txt')
        g = reader.read()
        for line in g:
            self.assertIsInstance(line, str)


if __name__ == '__main__':
    unittest.main()
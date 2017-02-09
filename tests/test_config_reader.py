# encoding:utf-8
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: chendonghua@baidu.com
Created time: 17/1/5 18:21
"""
import unittest
import configparser
import os

from config_reader import ConfReader

CONST_URL_FOR_LIST_FILE = 'test_dir_for_url'
CONST_DIR_FOR_OUTPUT = 'test_dir_for_output'
CONST_NUMBER_OF_MAX_DEPTH = 2232
CONST_NUMBER_OF_CRAWL_INTERVAL = 10
CONST_NUMBER_OF_TIMEOUT = 1034
CONST_NUMBER_OF_THREAD_COUNT = 16
CONST_TARGET_OF_URL_PATTERN = '*.jpeg | *.html'
CONST_NUMBER_OF_THREAD_COUNT = 14
CONST_NUMBER_OF_MAX_LINK = 80800


class TestConfigReader(unittest.TestCase):
    """
    ConfigReader测试类
    """
    def setUp(self):
        """
        测试前生成一个测试文件
        """
        file_name = 'test_file.cfg'
        dir_name = os.path.abspath(__file__)
        test_file_name = os.path.join(os.path.dirname(dir_name), file_name)
        config = configparser.ConfigParser()

        section_name = 'spider'

        config[section_name] = {
            'url_list_file': CONST_URL_FOR_LIST_FILE,
            'output_directory': CONST_DIR_FOR_OUTPUT,
            'max_depth': CONST_NUMBER_OF_MAX_DEPTH,
            'crawl_interval': CONST_NUMBER_OF_CRAWL_INTERVAL,
            'crawl_timeout': CONST_NUMBER_OF_TIMEOUT,
            'target_url': CONST_TARGET_OF_URL_PATTERN,
            'thread_count': CONST_NUMBER_OF_THREAD_COUNT,
            'max_link': CONST_NUMBER_OF_MAX_LINK
        }
        with open(test_file_name, 'w') as configfile:
            config.write(configfile)

        self._config_inst = ConfReader.instance(config_name=test_file_name)

        #print(self._config_inst.get_target_urls())

    def tearDown(self):
        """
        清除测试文件
        :return:
        """
        os.unlink('test_file.cfg')
        pass

    def test_single_instance(self):
        """
        单例有效性验证
        :return:
        """
        inst1 = ConfReader.instance()
        inst2 = ConfReader.instance()
        self.assertEqual(id(inst1), id(inst2))

    def test_read_thread_count(self):
        """
        :return:
        """
        self.assertEqual(self._config_inst.get_thread_count(),
                         CONST_NUMBER_OF_THREAD_COUNT)

    def test_read_interval(self):
        """
        :return:
        """
        self.assertEqual(self._config_inst.get_crawl_interval(),
                         CONST_NUMBER_OF_CRAWL_INTERVAL)

    def test_url_list_file(self):
        """
        :return:
        """
        self.assertEqual(self._config_inst.get_url_list_file(),
                         CONST_URL_FOR_LIST_FILE)

    def test_url_max_count(self):
        """
        :return:
        """
        self.assertEqual(self._config_inst.get_max_links_count(),
                         CONST_NUMBER_OF_MAX_LINK)

if __name__ == '__main__':
    unittest.main()
# encoding:utf-8
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: chendonghua@baidu.com
Created time: 17/1/12 18:46
"""
import unittest
import shutil
import os

from config_reader import ConfReader
from page_parser import PageParser

class TestPageParser(unittest.TestCase):
    """
    PageParser测试类
    """
    def tearDown(self):
        """
        清除测试生成的输出目录
        :return:
        """
        output_dir = ConfReader.instance().get_output_directory()
        if os.path.exists(output_dir):
            shutil.rmtree(ConfReader.instance().get_output_directory())

    def test_parse(self):
        """
        测试了三个场景：
        使用标准url
        使用无效url
        使用其他格式的url文档，如jpg
        :return:
        """
        #parser = Page_parser()
        url1 = 'http://pycm.baidu.com:8081/page1.html'
        expect_sub_url = 'http://pycm.baidu.com:8081/1/page1_1.html'
        parser = PageParser(url1)
        links = parser.parse()
        self.assertIn(expect_sub_url, links)

        url2 = 'http://pycm.baidu.com:8081/page7.html'
        parser = PageParser(url2)
        links = parser.parse()
        self.assertEqual(links, set())

        url3 = 'http://pycm.baidu.com:8081/3/image.jpg'
        parser = PageParser(url3)
        self.assertEqual(parser.parse(), set())

    def test_url_read(self):
        """
        测试了三个场景：
        使用标准url
        使用无效url
        使用其他格式的url文档，如jpg
        :return:
        """
        url1 = 'http://pycm.baidu.com:8081/page1.html'
        parser = PageParser(url1)
        content1 = parser.url_read()
        self.assertEqual(content1.__contains__('page1_4.html'), True)
        self.assertEqual(content1.__contains__('page1_1.html'), True)

        #invalid url test
        url2 = 'http://pycm.baidu.com:8081/page7.html'
        parser = PageParser(url2)
        content2 = parser.url_read()
        self.assertEqual(content2, '', "return content should be empty")

        #No support url test
        url3 = 'http://pycm.baidu.com:8081/3/image.jpg'
        parser = PageParser(url3)
        content3 = parser.url_read()
        self.assertEqual(content3, '')
        self.assertLogs(logger='../logs/spider.log', level='error')

if __name__ == '__main__':
    unittest.main()
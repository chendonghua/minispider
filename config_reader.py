# encoding:utf-8
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: chendonghua@baidu.com
Created time: 16/11/23 16:52
"""
import configparser
import os
from logger import logger


class ConfReader(object):
    """
    Conf Reader
    """

    @classmethod
    def instance(cls, config_name='spider.cfg'):
        """
        配置文件读取，使用单例方式，只读一次，放在内存中
        :param config_name: 配置文件名，无需指定路径，只要文件名即可
        :return:
        """
        if not hasattr(cls, "_instance"):
            cls._instance = cls(config_name)
        return cls._instance

    def __init__(self, config_name):
        dir_name = os.path.abspath(__file__)
        self._conf_dir = os.path.join(os.path.dirname(dir_name), 'conf')
        self._url_list_file = "./urls"
        self._output_directory = "./output"
        self._max_depth = 1
        self._crawl_interval = 1
        self._crawl_timeout = 1
        self._target_urls = ".*.(htm|html)"
        self._thread_count = 4
        self._max_links_count = 10000
        self.__read_confs(config_name)

    def __read_confs(self, file_name):

        config = configparser.ConfigParser()
        config.read(os.path.join(self._conf_dir, file_name), encoding='utf-8')

        section_name = 'spider'
        if section_name not in config.sections():
            #loger error message
            logger.warning("Read conf failed. Used default values")
            return
        else:
            self._url_list_file = config.get(section_name, "url_list_file")
            self._output_directory = config.get(section_name, "output_directory")
            self._max_depth = config.getint(section_name, "max_depth")
            self._crawl_interval = config.getint(section_name, "crawl_interval")
            self._target_urls = config.get(section_name, "target_url")
            self._thread_count = config.getint(section_name, "thread_count")
            self._max_links_count = config.getint(section_name, "max_link")

    def get_url_list_file(self):
        """
        :return: 种子文件的路径 string
        """
        return self._url_list_file

    def get_output_directory(self):
        """
        抓取结果存储目录
        :return: string
        """
        return self._output_directory

    def get_max_depth(self):
        """
        最大抓取深度
        :return: int
        """
        return self._max_depth

    def get_crawl_interval(self):
        """
        线程抓取间隔，当间隔时间内抓取量超过一定数量时，线程沉睡一定的间隔时间
        :return: int 单位秒(s)
        """
        return self._crawl_interval

    def get_target_urls(self):
        """
        目标url的正则匹配模式
        :return: string
        """
        return self._target_urls

    def get_thread_count(self):
        """
        开启的线程数量
        :return: int
        """
        return self._thread_count

    def get_max_links_count(self):
        """
        每次间隔时间内的链接抓取量
        :return: int
        """
        return self._max_links_count

if __name__ == '__main__':
    ths = ConfReader.instance().get_thread_count()
    print(ths)
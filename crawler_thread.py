# encoding:utf-8
################################################################################
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Author: chendonghua@baidu.com
Created time: 16/12/23 16:52
"""

import threading

from logger import logger
from config_reader import ConfReader
from page_parser import PageParser

from threading import RLock
from queue import Queue
from time import sleep


class CrawlerThread(threading.Thread):
    """
    负责页面的抓取线程

    Attributes:
        q： 种子队列
    """
    def __init__(self, q):
        super(CrawlerThread, self).__init__()
        self._q = q
        self._lock = RLock()
        self.daemon = True

    def crawl(self, url_q):
        """
        spider的爬取逻辑， 调用page_retriever解析下载url, 将提取的子url返回来
        并进行去重，加到队列中
        :param url_q: 待解析的url地址，绝对路径
        :return:
        """
        if not isinstance(url_q, tuple):
            print("Type error")
            return

        if CrawlerThreadPool.interval_links_cnt > \
                ConfReader.instance().get_max_links_count():
            interval = ConfReader.instance().get_crawl_interval()
            if interval == 0:
                interval = 60 * 5 # default every 5 minutes

            logger.info("Thread %s begin to sleep, %d s later continue" %
                        (threading.currentThread().getName(), interval))
            print("Waiting for %d seconds ..." % interval)
            sleep(interval)

            #重新计数
            self._lock.acquire()
            CrawlerThreadPool.interval_links_cnt = 0
            self._lock.release()
        else:
            pass

        (url, depth) = url_q
        if depth > ConfReader.instance().get_max_depth():
            print("Depth exceed. The max depth is {}".format(depth - 1))
            return
        page_parser = PageParser(url)
        links = page_parser.parse()
        new_links = links.difference(CrawlerThreadPool.seen_urls)
        for new_link in new_links:
            self._q.put((new_link, depth + 1))

        #statistic links number
        self._lock.acquire()
        CrawlerThreadPool.total_links += len(new_links)
        CrawlerThreadPool.interval_links_cnt += len(new_links)
        print("Spider have crawl {} links."
              .format(CrawlerThreadPool.total_links))
        CrawlerThreadPool.seen_urls.update(new_links)
        self._lock.release()

    def run(self):
        """
        main crawl task
        :return:
        """
        while True:
            url = self._q.get()
            if url is None:
                break
            self.crawl(url)
            self._q.task_done()


class CrawlerThreadPool(object):
    """
    管理线程的类
    """
    seen_urls = set()  # 已经访问过的链接集合
    interval_links_cnt = 0  # 间隔时间内的链接计数
    total_links = 0 #总链接数
    crawl_depth = 0

    def __init__(self, url=None, config_name=None):
        self._thread_count = ConfReader.instance(config_name).get_thread_count()
        self._url_queue = Queue()
        self._url_queue.put((url, 0))  # initialize: At first ,there is at least one url

    def add_seed(self, url):
        """
        添加种子url到队列
        :param url: 要添加的url
        :return:
        """
        self._url_queue.put((url, 0))

    def begin(self):
        """
        Created specified threads, then start all
        :return:
        """
        crawlers = []
        print("{} threads will be created".format(self._thread_count))
        for i in range(self._thread_count):
            crawler = CrawlerThread(self._url_queue)
            crawlers.append(crawler)
            crawler.start()

        self._url_queue.join()

        for i in range(self._thread_count):
            self._url_queue.put(None)

        for crawler in crawlers:
            crawler.join()

        print("Spider totally crawled %d links" % CrawlerThreadPool.total_links)

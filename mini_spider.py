# encoding:utf-8
"""
Author: cdhmuer333@126.com
Created time: 16/12/28 15:05
"""
from optparse import OptionParser

from crawler_thread import CrawlerThreadPool
from seedfile_reader import SeedFileReader

from time import time

VERSION = "1.0"

def main():
    """
    main 方法
    """
    parser = OptionParser(usage="%prog [-f] [-q]",
                          version="%prog-{}".format(VERSION))
    parser.add_option("-c", dest="conf", type="string",
                      help="Specify a conf file")

    (options, args) = parser.parse_args()

    seed_file = SeedFileReader()
    if not options.conf:
        print("You have no specified any conf file. Using default conf file")

    pool = CrawlerThreadPool(config_name=options.conf)
    g = seed_file.read()
    for seed in g:
        seed = seed.strip('\n')
        pool.add_seed(seed)
    pool.begin()

if __name__ == '__main__':
    start_time = time()
    main()
    end_time = time()
    print("Spend time {} seconds".format(round(end_time - start_time, 2)))

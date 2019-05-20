# -*- coding: utf-8 -*-
'''
Created on 2019-05-20
@author: zhengjin
'''

import os
import re
import sys
sys.path.append(os.getenv('PYPATH'))

from appdemos import CrawlHtml
from utils import Constants, LogManager, HttpUtils


def crawl_pages_count():
    url = 'http://www.522yw.city/article/list_3.html'
    crawl = CrawlHtml(url)
    last_page = crawl.get_html_obj_by_css('.pagelist a:last')
    results = re.match('list_3_(.*).html', last_page.attr('href'))
    return results.group(1)


def crawl_article_links_of_page(url):
    crawl = CrawlHtml(url)
    links = crawl.get_html_obj_by_css('.text1_1text .list a').items()
    return [link.attr('href') for link in links]


def crawl_images_of_page(url):
    crawl = CrawlHtml(url)
    images = crawl.get_html_obj_by_css('.centen2 img').items()
    return ['http://www.522yw.city' + img.attr('src') for img in images]


def download_images(url, dir_path):
    pass


def crawl_images_main():
    count = crawl_pages_count()

    url = 'http://www.522yw.city/article/list_3_2.html'
    urls = crawl_article_links_of_page(url)

    img_urls = crawl_images_of_page(urls[0])
    print(img_urls)


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    crawl_images_main()
    print('crawl images demo DONE!')

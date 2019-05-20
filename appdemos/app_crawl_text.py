# -*- coding: utf-8 -*-
'''
Created on 2019-05-20
@author: zhengjin
'''

import os
import sys
from pyquery import PyQuery as pq
sys.path.append(os.getenv('PYPATH'))

from utils import Constants
from utils import HttpUtils
from utils import LogManager


class CrawlHtml(object):

    def __init__(self, url, query, method=HttpUtils.HTTP_METHOD_GET):
        self.url = url
        self.query = query
        self.method = method
        self.html_dom = None

    def get_html_dom(self):
        if self.html_dom is None:
            self._parse_html_dom()
        return self.html_dom

    def get_html_obj_by_css(self, selector):
        if self.html_dom is None:
            self._parse_html_dom()
        return self.html_dom(selector)

    def _parse_html_dom(self):
        content = self._get_html_content()
        self.html_dom = pq(content)

    def _get_html_content(self):
        http_utils = HttpUtils.get_instance()
        resp = http_utils.send_http_request(self.method, self.url, self.query, timeout=0.5)
        return resp.content.decode(encoding='utf-8')


def crawl_article_titles_of_page(url, query):
    crawl = CrawlHtml(url, query)
    selector = '.panel-body.item-list>div .title.media-heading>a'
    title_elements = crawl.get_html_obj_by_css(selector).items()
    return [ele.attr('title') for ele in title_elements]


def crawl_pages_count(url):
    query = 'page=1'
    crawl = CrawlHtml(url, query)

    pages_elemnts = crawl.get_html_obj_by_css('.pagination>li>a').items()
    pages_list = [ele for ele in pages_elemnts]
    return pages_list[len(pages_list) - 2].text()


def crawl_text_main():
    from concurrent.futures import ProcessPoolExecutor
    from concurrent.futures import wait
    
    url = 'https://testerhome.com/topics'
    count = crawl_pages_count(url)

    executor = ProcessPoolExecutor(max_workers=3)
    page_numbers = [i for i in range(0, int(count)) if i % 5 == 0]
    furtures = [executor.submit(crawl_article_titles_of_page, url, 'page=%d' % num)
                for num in page_numbers]
    furtures_done = wait(furtures, return_when='ALL_COMPLETED')

    all_titles = []
    for f in furtures_done.done:
        all_titles.extend(f.result())

    print('TESTING ARTICLE TITLES:')
    for titles in all_titles:
        print(titles)


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    crawl_text_main()
    print('crawl text (article titles) demo DONE!')

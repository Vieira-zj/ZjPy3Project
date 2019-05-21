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


class CrawlImages(object):

    def __init__(self):
        self._logger = LogManager.get_logger()

    def crawl_pages_count(self, url):
        last_page = CrawlHtml.get_instance().fetch_html_content(url) \
            .get_ui_element_by_css('.pagelist a:last')
        results = re.match('list_3_(.*).html', last_page.attr('href'))
        return results.group(1)


    def crawl_article_links_of_page(self, url):
        links = CrawlHtml.get_instance().fetch_html_content(url) \
            .get_ui_element_by_css('.text1_1text .list a').items()
        return [link.attr('href') for link in links]


    def crawl_page_images_process(self, url):
        save_dir_path = os.path.join(os.getenv('HOME'), 'Downloads/tmp_files/crawl_images')

        img_urls = self.crawl_image_urls_of_page(url)
        for url in img_urls:
            self.download_and_save_images(url, save_dir_path)


    def crawl_image_urls_of_page(self, url):
        images = CrawlHtml.get_instance().fetch_html_content(url) \
            .get_ui_element_by_css('.centen2 img').items()
        return ['http://www.522yw.city' + img.attr('src') for img in images]


    def download_and_save_images(self, url, save_dir_path):
        items = url.split('/')
        file_name = items[len(items) - 1]
        save_path = os.path.join(save_dir_path, file_name)

        if os.path.exists(save_path):
            return
        # CrawlHtml.get_instance().get_and_save_files(url, save_path)


    def crawl_images_main(self):
        from concurrent.futures import ProcessPoolExecutor
        from concurrent.futures import wait

        home_url = 'http://www.522yw.city/article/list_3.html'
        count = self.crawl_pages_count(home_url)

        base_url = 'http://www.522yw.city/article/list_3_%d.html'
        page_urls = [home_url]
        page_urls.extend([base_url % i for i in range(1, int(count)) if i == 1])

        total_article = 0
        f_submit = []
        executor = ProcessPoolExecutor(max_workers=3)
        for page_url in page_urls:
            article_urls = self.crawl_article_links_of_page(page_url)
            total_article += len(article_urls)
            f_submit.extend([executor.submit(self.crawl_page_images_process, url)
                            for url in article_urls])

        f_done = wait(f_submit, return_when='ALL_COMPLETED')

        self._logger.info('\n\nSUMMARY:')
        self._logger.info('number of %d tasks (for pages) done.' % len(f_done))
        self._logger.info('crawl article count: ' + str(total_article))


if __name__ == '__main__':

    LogManager.build_logger(Constants.LOG_FILE_PATH)
    CrawlImages().crawl_images_main()
    LogManager.clear_log_handles()
    print('crawl images demo DONE!')

# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re

import time


class A275Spider(scrapy.Spider):
    name = '275'
    allowed_domains = ['baoting.hainan.gov.cn']
    start_urls = ['http://baoting.hainan.gov.cn/baoting/xxgk/filesearch.html?siteid=51&currpage=1&pagesize=20&title=&content=&filenum=&pubdate=']

    #
    # chrome_options = Options()
    # # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option('prefs', prefs)
    # chrome_driver_path = 'F:\Workspace\python\lab_scrapy\spider_crawl_start_55\scrapy_spider\scrapy_spider\chromedriver.exe'
    # driver = None
    #
    # # set parse func to launch webdriver
    # def parse(self, response):
    #     self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, chrome_options=self.chrome_options)
    #     yield scrapy.Request(url=response.url, callback=self.launch_driver_get)
    #
    # def launch_driver_get(self, response):
    #     self.driver.get(url=self.start_urls[0])
    #
    #     print(">>>>>>>>>>>>   ", self.driver.page_source)
    #
    #     # table_url_list = self.driver.find_elements_by_xpath('//*[@id="tablist"]/tbody//tr/td[2]/a')
    #     # for tu in table_url_list:
    #     #     print(">>>>>>>>>   ", tu.get_attribute('href'))
    #
    #     time.sleep(5)
    #     self.driver.quit()

    def parse(self, response):
        post_data = {
                        "title": '',
                        "content": '',
                        "filenum": '',
                        "pubdate": '',
                        "siteid": '51',
                        "pagesize": '20',
                        "currpage": '3'
        }

        # post_data = "title=&content=&filenum=&pubdate=&siteid=51&pagesize=20&currpage=2"
        yield scrapy.FormRequest(url="http://baoting.hainan.gov.cn/hnsearch/xxgkadvance/", formdata=post_data, callback=self.post_test)


    def post_test(self, response):
        print("??????????   ", response.url)
        table_url_list = response.xpath('//*[@id="tablist"]/tbody//tr/td[2]/a/@href').extract()
        print(table_url_list)






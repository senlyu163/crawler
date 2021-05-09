# # -*- coding: utf-8 -*-
# import scrapy
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# from ..items import ScrapySpiderItem
# from ..utils import extract_CN_from_content
# import re
# import time
#
# class A119Spider(scrapy.Spider):
#     name = '119'
#     allowed_domains = ['hlraohe.gov.cn']
#     start_urls = ['http://www.hlraohe.gov.cn/newslist/newslist_all_zwgk.jsp?fjlm=24184&lmid=24238']
#
#     chrome_options = Options()
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--disable-gpu')
#     # prefs = {"profile.managed_default_content_settings.images": 2}
#     # chrome_options.add_experimental_option('prefs', prefs)
#     chrome_driver_path = 'F:\Workspace\python\lab_scrapy\spider_crawl_start_55\scrapy_spider\scrapy_spider\chromedriver.exe'
#     driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)
#
#     def parse(self, response):
#         yield scrapy.Request(url=self.response.url, callback=self.click_nxt_button)
#
#     def click_nxt_button(self, response):
#         page_num = self.driver.find_element_by_xpath('//div[@class="pagelist"]/span[2]/strong')
#         page_num_text = page_num.text
#         page_nums = re.search(r"/(\d+)", page_num_text).groups()[0]
#         yield scrapy.Request(url=response.url, callback=self.extract_table_url)
#
#         for _ in range(page_nums-1):
#             time.sleep(1)
#             self.driver.find_element_by_xpath('//div[@class="pagelist"]/a[2]').click()
#             time.sleep(2)
#             nxt_url = self.driver.current_url
#             yield scrapy.Request(url=nxt_url, callback=self.click_nxt_button)
#
#     def extract_table_url(self, response):
#         table_urls = response.xpath('//ul[@class="newlist hastime"]//li/a/@href').extract()
#         for tu in table_urls:
#             yield scrapy.Request(url=tu, callback=self.extract_context)
#
#     def extract_context(self, response):
#         item = ScrapySpiderItem()
#         item['url'] = response.url
#
#         date = response.xpath('/html/body/div[4]/div[1]/h2/span[3]/text()').extract_first()
#         date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
#         item['date'] = date
#
#         title = response.xpath('/html/body/div[4]/div[1]/h1/text()').extract_first()
#         item['title'] = title
#
#         contents = response.xpath('//div[@class="article"]').extract()
#         item['contents'] = extract_CN_from_content(contents)
#         return item
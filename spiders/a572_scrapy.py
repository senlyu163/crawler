# -*- coding: utf-8 -*-
import scrapy
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A572ScrapySpider(scrapy.Spider):
    name = '572_scrapy'
    allowed_domains = ['xjwqx.gov.cn']
    start_urls = ['http://www.xjwqx.gov.cn/gkindex.htm',
                  'http://www.xjwqx.gov.cn/gkbmlb.htm']

    def parse(self, response):
        navi_list = response.xpath('//ul[@class=" am-avg-sm-2 am-thumbnails"]//li/a/@href').extract()
        for nl in navi_list:
            complete_url = response.urljoin(nl)
            yield scrapy.Request(url=complete_url, callback=self.extract_iframe)

        item_iframe_url = response.xpath('//iframe[@id="rightFrame"]/@src').extract_first()
        yield scrapy.Request(url=response.urljoin(item_iframe_url), callback=self.extract_gk_items)

    def extract_gk_items(self, response):
        items_url = response.xpath('//div[@class="am-u-lg-12"]/div//div/div/ul//li/a/@href').extract()
        for iu in items_url:
            complete_url = response.urljoin(iu)
            yield scrapy.Request(url=complete_url, callback=self.extract_iframe)


    def extract_iframe(self, response):
        iframe_url = response.xpath('//iframe/@src').extract()
        # print("url:", response.url, "   >>>>>>>>>>>> :", iframe_url)
        for iu in iframe_url:
            complete_iframe = response.urljoin(iu)
            yield scrapy.Request(url=complete_iframe, callback=self.extract_header_catagory_urls)

    def extract_header_catagory_urls(self, response):
        hc_list = response.xpath('//div[@id="node-items"]//a/@href').extract()
        for hc in hc_list:
            complete_node_url = response.urljoin(hc)
            yield scrapy.Request(url=complete_node_url, callback=self.extract_table_urls)

    def extract_table_urls(self, response):
        table_urls = response.xpath('//*[@id="gk_list_table"]//tr/td[2]/a/@href').extract()
        for tu in table_urls:
            complete_table = response.urljoin(tu)
            yield scrapy.Request(url=complete_table, callback=self.extract_context)

        # next page
        nxt_page = response.xpath('//*[@id="list"]/div[2]/div/div/ul/li[5]/a/@href').extract_first()
        # print("<<<<<<<<<<<<<<<<<<    ", nxt_page)
        complete_nxt_url = response.urljoin(nxt_page)
        # print("         <>><><><><><><><><>><><><><>>   ", complete_nxt_url)
        yield scrapy.Request(url=complete_nxt_url, callback=self.extract_table_urls)

    def extract_context(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="gk-info"]/tr[4]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="gk-info"]/tr[2]/td[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="text"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

# -*- coding: utf-8 -*-
import scrapy
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
import time

class A175ScrapySpider(scrapy.Spider):
    name = '175_scrapy'
    allowed_domains = ['hnhx.gov.cn']
    start_urls = ['http://www.hnhx.gov.cn/xxgk.htm']

    url_template = "http://www.hnhx.gov.cn/xxgk-ssjgy.jsp?ainfolist112372t=1106&ainfolist112372p={}&ainfolist112372c=10&gitcatcode=&fgidate=&lgidate=&wbtreeid=1078&giindentifier=&giscatcode=+&urltype=egovinfo.EgovSearchList&gicategorycode=&stype=advance&giccode=&gipubcode=+&gititle=&gidocno="
    # page_num = 1

    def parse(self, response):
        # url = self.url_template.format(self.page_num)
        # yield scrapy.Request(url=url, callback=self.extract_table_urls)

        for n in range(1106):
            time.sleep(2)
            url = self.url_template.format(n+1)
            yield scrapy.Request(url=url, callback=self.extract_table_urls)

        # self.page_num += 1
        # time.sleep(2)
        # yield scrapy.Request(callback=self.parse)

    def extract_table_urls(self, response):
        url_list = response.xpath('//*[@id="ainfolist112372"]/div[1]/table/tbody/table//tr/td[2]/span/a/@href').extract()
        for ul in url_list:
            time.sleep(2)
            complete_url = response.urljoin(ul)
            yield scrapy.Request(url=complete_url, callback=self.extract_content)

    def extract_content(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//td[@style="background-color: #fffcf6;border: 1px solid #edc77b;padding-top: 3px;padding-right: 4px;padding-left: 4px;vertical-align: top;height: 60px"]/table/tr/td[6]/text()').extract_first()
            date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
            item['date'] = date

            title = response.xpath('//td[@style="TEXT-ALIGN: center;LINE-HEIGHT: 200%;FONT-FAMILY: 宋体;HEIGHT: 26px;COLOR: #222222;FONT-SIZE: 14pt;FONT-WEIGHT: bold"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="egovinfocontenttable"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//span[@class="timestyle112078"]/text()').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//td[@class="titlestyle112078"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//*[@id="vsb_content_500"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item

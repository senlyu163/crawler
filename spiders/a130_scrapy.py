# -*- coding: utf-8 -*-
import scrapy
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A130ScrapySpider(scrapy.Spider):
    name = '130_scrapy'
    allowed_domains = ['susong.gov.cn']
    start_urls = ['http://www.susong.gov.cn/public/User/PageInfo.aspx?unitId=4&clsid=0']

    def start_requests(self):
        headers = {'User-Agent':'User-Agent:Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:69.0)Gecko/20100101Firefox/69.0'}
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, headers=headers)

    def parse(self, response):
        iframe_url = response.xpath('//iframe/@src').extract_first()
        yield scrapy.Request(url=response.urljoin(iframe_url), callback=self.extract_table_urls)

    def extract_table_urls(self, response):
        table_urls = response.xpath('/html/body/div[2]/table//tr/td[3]').extract()
        for tu in table_urls:
            complete_url = response.urljoin(tu)
            yield scrapy.Request(url=complete_url, callback=self.extract_context)

        nxt_page = response.xpath('//div[@class="Pages"]/span[3]/a/@href').extract_first()
        yield scrapy.Request(url=response.urljoin(nxt_page), callback=self.extract_table_urls)

    def extract_context(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="container"]/div/div[2]/table/tbody/tr[3]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="container"]/div/div[2]/table/tbody/tr[5]/td[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@id="artibody"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

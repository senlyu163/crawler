# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A280Spider(CrawlSpider):
    name = '280'
    allowed_domains = ['cqfd.gov.cn']
    start_urls = [
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zcwj/xzgfxwj/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zcwj/xzfwj/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/zcjd/',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/xzsyxsf/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/czyjs/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zfcg/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/fptp/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/gsgg/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/jjyx/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/ghjh/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/sthj/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/ggws/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/jgysf/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/tjxx/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/gtfg/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/yjgl/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/spypaq/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/aqsc/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/msbz/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/zdlyxxgk/jycy/list.html',
        'http://www.cqfd.gov.cn/zwgk_200/fdzdgknr/gcjslyxm/list.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'list_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div/table/tbody/tr[4]/td[4]').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[3]/div/div/div[1]/p/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zwxl-article"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

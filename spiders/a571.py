# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
import requests

class A571Spider(CrawlSpider):
    name = '571'
    allowed_domains = ['xjahq.gov.cn']
    start_urls = [
        'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10376',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10377',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?cat_id=10741',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10387',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10388',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10380',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10378',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10383',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10847',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10974',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfgw&cat_id=10975',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfpb&cat_id=10410',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfpb&cat_id=10411',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfpb&cat_id=10412',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfpb&cat_id=10851',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfpb&cat_id=10853',
        'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKfpb&cat_id=10413',
        'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKjyj&cat_id=10448',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKjyj&cat_id=10449',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKjyj&cat_id=10452',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKjyj&cat_id=10451',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKjyj&cat_id=10450',
        # 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKjyj&cat_id=10453',
        'http://www.xjahq.gov.cn/info/iList.jsp?cat_id=10849&cur_page=1',
        'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKczj&cat_id=10295',
        'http://www.xjahq.gov.cn/info/iList.jsp?tm_id=9',
    ]

    # url_template = 'http://www.xjahq.gov.cn/info/iList.jsp?isSd=false&node_id=GKczj&cat_id={}'
    # for n in range(10100, 10600):
    #     url = url_template.format(n)
    #     if requests.get(url=url).status_code == int('200'):
    #         start_urls.append(url)
    #     else:
    #         continue

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="node-items"]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="list"]/div/div//div/div/ul//li'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="gk_list_table"]//tr/td[1]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="list"]/div[2]/div/div/ul/li[5]'), follow=True),
        # Rule(LinkExtractor(allow=r'\?node_id=GKrmzf&site_id=CMSahqx&cat_id=\d+&cur_page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'\?cat_id=\d+&cur_page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="gk-info"]/tr[4]/td[4]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="text"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="tableinfo"]/tr/td[2]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="title"]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@id="text"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item

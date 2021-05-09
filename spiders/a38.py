# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest


class A38Spider(CrawlSpider):
    name = '38'
    allowed_domains = ['xxgk.hengshui.gov.cn']  # raoyang xian
    # start_urls = ['http://xxgk.hengshui.gov.cn/eportal/ui?pageId=793458&currentPage=2&moduleId=9759&formKey=GOV_OPEN&columnName=EXT_STR7&relationId=']
    # start_urls = ['http://xxgk.hengshui.gov.cn/hssryx/2637135/zc34/gfxwj1597/index.html']
    start_urls = ['http://xxgk.hengshui.gov.cn/eportal/ui?pageId=2637137&currentPage=1&moduleId=d4f52ddd87394823a02268c8dbca25e3']

    for i in range(525):
        template_url = 'http://xxgk.hengshui.gov.cn/eportal/ui?pageId=2637137&currentPage={}&moduleId=d4f52ddd87394823a02268c8dbca25e3'.format(i)
        start_urls.append(template_url)

    rules = (
        Rule(LinkExtractor(allow=r'/hssryx/.*/index.html'), callback='splash_get', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # def start_requests(self):
    #     for url in self.start_urls:
    #         # Splash 默认是render.html,返回javascript呈现页面的HTML。
    #         yield SplashRequest(url, args={'wait': 1})

    def splash_get(self, response):
        yield SplashRequest(url=response.url, callback=self.parse_item, args={'wait': 2})

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[3]/div[2]/div/div[3]/div/div[2]/div/p/span[3]').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath(
            '/html/body/div[3]/div[2]/div/div[3]/div/div[2]/div/h3').extract_first()
        item['title'] = title

        contents = response.xpath('/html/body/div[3]/div[2]/div/div[3]/div/div[2]/div/div/div').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

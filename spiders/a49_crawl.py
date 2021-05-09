# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapySpiderItem
from ..utils import extract_CN_from_content
import re
from scrapy_splash import SplashRequest


class A49CrawlSpider(CrawlSpider):
    name = '49_crawl'
    allowed_domains = ['youyuzf.gov.cn']
    start_urls = ['http://www.youyuzf.gov.cn/zwgk/zwgw/', 'http://www.youyuzf.gov.cn/zwgk/gggs/',
                  'http://www.youyuzf.gov.cn/zwgk/jhzj/']

    for i in range(8):
        next_page_url = "http://www.youyuzf.gov.cn/zwgk/zwgw/index_{}.html".format(i + 1)
        start_urls.append(next_page_url)

    for i in range(28):
        next_page_url = 'http://www.youyuzf.gov.cn/zwgk/gggs/index_{}.html'.format(i + 1)
        start_urls.append(next_page_url)

    for i in range(2):
        next_page_url = 'http://www.youyuzf.gov.cn/zwgk/jhzj/index_{}.html'.format(i + 1)
        start_urls.append(next_page_url)

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//ul[@class="navbar"]//li/h4'), follow=True),
    #     Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
    #     Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
    #     # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div[3]/ul/li/h2/a[2]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div[3]/ul//li/h2/a[1]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div[3]/a[3]'), callback='start_requests', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div[3]/a[3]'), callback='add_to_start_urls', follow=True),
        # Rule(LinkExtractor(allow=r'/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # def _build_request(self, rule, link):
    #     r = SplashRequest(url=link.url, args={"wait": 1.5})
    #     r.meta.update(rule=rule, link_text=link.text)
    #     return r

    # def add_to_start_urls(self):
    #     for i in range(8):
    #         next_page_url = "http://www.youyuzf.gov.cn/zwgk/zwgw/index_{}.html".format(i + 1)
    #         self.start_urls.append(next_page_url)
    #
    #     for i in range(28):
    #         next_page_url = 'http://www.youyuzf.gov.cn/zwgk/gggs/index_{}.html'.format(i + 1)
    #         self.start_urls.append(next_page_url)
    #
    #     for i in range(2):
    #         next_page_url = 'http://www.youyuzf.gov.cn/zwgk/jhzj/index_{}.html'.format(i + 1)
    #         self.start_urls.append(next_page_url)

    # def start_requests(self):
    #     for url in self.start_urls:
    #         # Splash 默认是render.html,返回javascript呈现页面的HTML。
    #         yield SplashRequest(url, args={'wait': 2})


    # def _build_request(self, rule_index, link):
    #     return SplashRequest(
    #         url=link.url,
    #         callback=self._callback,
    #         errback=self._errback,
    #         meta=dict(rule=rule_index, link_text=link.text),
    #     )

    # def _requests_to_follow(self, response):
    #     # if not isinstance(response, HtmlResponse):
    #     #     return
    #     seen = set()
    #     for n, rule in enumerate(self._rules):
    #         links = [lnk for lnk in rule.link_extractor.extract_links(response)
    #                  if lnk not in seen]
    #         if links and rule.process_links:
    #             links = rule.process_links(links)
    #         for link in links:
    #             seen.add(link)
    #             r = self._build_request(n, link)
    #             yield rule.process_request(r)

    # def start_requests(self):
    #     for url in self.start_urls:
    #         # Splash 默认是render.html,返回javascript呈现页面的HTML。
    #         yield SplashRequest(url, args={'wait': 3})

    def parse_item(self, response):
        # print("@@@@@@@@@@@@@@@@@ ", response.url)
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div[2]/div[1]/p/span').extract_first()
        date = re.search(r"(\d{4}年\d{2}月\d{2}日)", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div[2]/div[1]/h1/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="TRS_Editor"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

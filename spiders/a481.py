# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A481Spider(CrawlSpider):
    name = '481'
    allowed_domains = ['wubu.gov.cn']
    start_urls = [
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10067',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10306',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10066',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10094',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10083',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=13081',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10115',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=13094',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10069',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10072',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=13086',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=12670',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=10073',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=13095',
        'http://www.wubu.gov.cn/info/iList.jsp?site_id=CMSwubu&cat_id=12669',
    ]

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//table[@class="list_table"]//tr/td[2]'), follow=True),
        # Rule(LinkExtractor(allow=r'/info/iList\.jsp\?tm_id=\d+&cat_id=\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/xxgk/[a-z]+/[a-z]+/\d+\.htm$'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\?site_id=CMSwubu&cat_id=.*cur_page=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )
    #
    # def _build_request(self, rule, link):
    #     r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5})
    #     r.meta.update(rule=rule, link_text=link.text)
    #     return r
    #
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

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="info_content"]/div[9]/table/tbody/tr[1]/td[6]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="info_content"]/div[4]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="info_content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="info_content"]/div[9]/table/tbody/tr[4]/td[4]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="info_content"]/div[4]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="info_content"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item

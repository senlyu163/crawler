# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A479Spider(CrawlSpider):
    name = '479'
    allowed_domains = ['mizhi.gov.cn']
    start_urls = ['http://www.mizhi.gov.cn/news_list.rt?descriptionNumber=50&modelId=4&sort=3&channlCid=0&channlId=50&channlSn=13_2zec_21bl9_501gi&titleNumber=30&pageNo=3']

    # url_template = "http://www.mizhi.gov.cn/zwgk_list.rt?descriptionNumber=50&modelId=4&sort=3&channlCid=0&channlId=13&channlSn=13_2zec&titleNumber=30&pageNo={}"
    # for n in range(160):
    #     url = url_template.format(n+1)
    #     start_urls.append(url)

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="zwlist_nr"]/ul//li/div[2]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/news_list.*pageNo=\d+'), follow=True),

        Rule(LinkExtractor(allow=r'/html/zwgk/[a-z]+/[a-z]+/index\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/[a-z]+/[a-z]+/\d+/\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/news_list.*pageNo=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 0.5})
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def _requests_to_follow(self, response):
        # if not isinstance(response, HtmlResponse):
        #     return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def parse_item(self, response):
        try:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('//*[@id="pageThree"]/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/td[4]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="pageThree"]/div[2]/div[2]/div/div[2]/div[2]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="xwnr"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath(
                '//*[@id="pageThree"]/div[2]/div[2]/div/div[1]/div[4]/span[1]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('//*[@id="pageThree"]/div[2]/div[2]/div/div[1]/div[2]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="xwnr"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item

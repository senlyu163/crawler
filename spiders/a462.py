# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A462Spider(CrawlSpider):
    name = '462'
    allowed_domains = ['pucheng.gov.cn']
    start_urls = [
        'http://www.pucheng.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=473&catalog_id=473',
        'http://www.pucheng.gov.cn/info/iList.jsp?isSd=false&node_id=&cat_id=496&catalog_id=496',
    ]

    url_template_1 = "http://www.pucheng.gov.cn/info/iList.jsp?tm_id=345&node_id=&site_id=CMSpc&catalog_id=473&cur_page={}"
    for n in range(85):
        url = url_template_1.format(n+1)
        start_urls.append(url)

    url_template_2 = "http://www.pucheng.gov.cn/info/iList.jsp?tm_id=345&node_id=&site_id=CMSpc&catalog_id=496&cur_page={}"
    for n in range(147):
        url = url_template_2.format(n+1)
        start_urls.append(url)

    rules = (
        # Rule(LinkExtractor(allow=r'/info/iList\.jsp\?tm_id=\d+&cat_id=\d+'), follow=True),
        # Rule(LinkExtractor(allow=r'/gk/zwgk\d+/zwgk\d+/zwgk\d+/\d+\.htm'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'\?tm_id=\d+&node_id=&site_id=CMSpc&catalog_id=\d+&cur_page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/gk/.*/\d+\.htm'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div/div[4]'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    # def _build_request(self, rule, link):
    #     r = SplashRequest(url=link.url, callback=self._response_downloaded, args={"wait": 1.5})
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

            date = response.xpath('/html/body/div[3]/div[4]/table/tr/td[6]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div[2]/div/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item
        except:
            item = ScrapySpiderItem()
            item['url'] = response.url

            date = response.xpath('/html/body/div[3]/div[4]/table/tr[2]/td[4]').extract_first()
            date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
            item['date'] = date

            title = response.xpath('/html/body/div[3]/div[4]/table/tr[3]/td[2]/text()').extract_first()
            item['title'] = title

            contents = response.xpath('//div[@class="article"]').extract()
            item['contents'] = extract_CN_from_content(contents)
            return item

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from scrapy_splash import SplashRequest

class A333Spider(CrawlSpider):
    name = '333'
    allowed_domains = ['xsx.gov.cn']
    start_urls = [
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/zcwj/zcwj_5125894/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/zcwj/bmwj/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/zcwj/xgfz/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/zcwj/zdjcygk/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/zcwj/gfxwjba/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/zcwj/flfg_5623129/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/ghjh/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/tjxx/tjfx/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/tjxx/tjsj/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/tjxx/tjgb/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/yjgl/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/jcxxgk/jdjc/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/qzqd/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/czzj/czysjsgjf/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/czzj/czjsjsgjf/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/czzj/hmzj/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/czzj/czszqk/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/sjxx/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/tpgz/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/shbz/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/shfl/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/shgy/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/hjbh/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/jyxx/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ylws/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/snbt/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/jsjf/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/zdcq/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/tajy/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/zfcg/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/zdjsxm/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/zfcg/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ggzypz/bzxajgc/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ggzypz/bzxzf/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ggzypz/tdcr/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ggzypz/bdcdj/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/spypaq/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ylfw/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/jraq/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/shza/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/aqsc/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/scjg/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ggwhty/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/ggflfw/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/zhjz/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/shbx/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/szfw/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/lyscgl/',
        'http://www.xsx.gov.cn/zwgk/xxgkml/zdlyxx/fgfgg/',
    ]

    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//li[@class="xxgkTree"]/ul//li/ul//li/span'), follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/xxgkml/[a-z]+/[a-z]+/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/zwgk/xxgkml/[a-z]+/[a-z]+/[a-z]+_\d+/\d+/t\d+_\d+\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'index_\d+\.html'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        for su in self.start_urls:
            yield SplashRequest(url=su)

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
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[1]/div[2]/div[2]/div[4]/span[3]').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="content"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

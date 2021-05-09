# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re
from ..utils import gen_url

class A345Spider(CrawlSpider):
    name = '345'
    allowed_domains = ['gzxr.gov.cn']
    start_urls = [
        'http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/zcwj_44570/rff/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/czzj_44559/zfyjsjsgjf/zfysjsgjf/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/xzxxgk/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/zdxxgkzl_44557/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/czzj_44559/czzcxx/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/fpgz_44560/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/czzj_44559/zfyjsjsgjf/zfjsjsgjf/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/ggzypz_44564/czzfbzajgc_44616/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/ggzypz_44564/tdzy_44617/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/zcwj_44570/rzfbf/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/ghjh_44573/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/jcgk/index.html',
        'http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/xzxxgk/index.html',
    ]


    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/xzxxgk/index_{}.html"
    gen_url(11, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/zdxxgkzl_44557/index_{}.html"
    gen_url(7, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/czzj_44559/czzcxx/index_{}.html"
    gen_url(2, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/fpgz_44560/index_{}.html"
    gen_url(10, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/ggzypz_44564/czzfbzajgc_44616/index_{}.html"
    gen_url(1, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/ggzypz_44564/tdzy_44617/index_{}.html"
    gen_url(3, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/zcwj_44570/rzfbf/index_{}.html"
    gen_url(33, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/ghjh_44573/index_{}.html"
    gen_url(5, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/jcgk/index_{}.html"
    gen_url(2, url_template, start_urls)
    url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/jcgk_44556/xzxxgk/index_{}.html"
    gen_url(8, url_template, start_urls)
    # url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/hjbh_44567/yjjc_44619/index_{}.html"
    # gen_url(12, url_template)
    # url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/hjbh_44567/yjjc_44619/index_{}.html"
    # gen_url(12, url_template)
    # url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/hjbh_44567/yjjc_44619/index_{}.html"
    # gen_url(12, url_template)
    # url_template = "http://www.gzxr.gov.cn/xxgk/xxgkml/zdlygk_44555/hjbh_44567/yjjc_44619/index_{}.html"
    # gen_url(12, url_template)


    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="gkml"]/div/li[1]/div/div/div/ul//li/ul//li/span'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="idData"]//tr/td[3]'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//*[@id="barcon"]/div'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div/ul/li[4]/span').extract_first()
        date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/div/ul/li[7]/span/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//div[@class="zx_content t_l"]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item

    def prt_index(self, response):
        print(response.url)

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils import extract_CN_from_content
from ..items import ScrapySpiderItem
import re

class A140Spider(CrawlSpider):
    name = '140'
    allowed_domains = ['yuan.gov.cn']
    start_urls = [
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd2&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd3&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd4&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd5&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd6&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd7&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd8&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdd9&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdda&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abddb&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abddc&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abddd&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abdde&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abddf&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde0&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde1&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde2&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde3&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde4&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde5&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde6&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde7&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde8&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
        'http://www.yuan.gov.cn/opennessTarget/?branch_id=5c6a13a1463a6e63215a5992&branch_type=&column_code=&topic_id=5c6a7e9822ffaf66ca5abde9&tag=&open_type=&keywords=&from_date=&end_date=&query_type=',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="xxgk_navli"]/ul//li[3]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/opennessTarget/\?branch_id=.*&branch_type=&column_code=&topic_id=.*&tag=&open_type=&keywords=&from_date=&end_date=&query_type=&page=\d+'), follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//ul[@id="organ_class_3032981_tree"]//li'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapySpiderItem()
        item['url'] = response.url

        date = response.xpath('//*[@id="wenzhang"]/div[1]/table/tbody/tr[2]/td[2]/text()').extract_first()
        date = re.search(r"(\d{4}-\d{2}-\d{2})", date).groups()[0]
        item['date'] = date

        title = response.xpath('//*[@id="wenzhang"]/div[1]/table/tbody/tr[5]/td[1]/text()').extract_first()
        item['title'] = title

        contents = response.xpath('//*[@id="wenzhang"]/div[3]').extract()
        item['contents'] = extract_CN_from_content(contents)
        return item
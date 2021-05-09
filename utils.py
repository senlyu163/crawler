from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

def get_next_page_url(url, xpath):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_driver_path = '/home/sen/workspace/python/spider_crawl/chromedriver'
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)
    driver.get(url)
    driver.find_element_by_xpath(xpath).click()
    # time.sleep(1)
    return driver.current_url

def extract_CN_from_content(url_contents_all):
    contents_list = ''
    for tmp in url_contents_all:
        url_zh = re.findall(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]+', tmp)
        for i in url_zh:
            contents_list += i

    return contents_list

def add_url_to_start_url(url, index, start_urls):
    url_template = url[:-6] + "_{}" + url[-6:]
    for n in range(index):
        complete_url = url_template.format(n+1)
        start_urls.append(complete_url)

def gen_url(num, url_t, start_urls):
    for n in range(num):
        url = url_t.format(n+1)
        start_urls.append(url)
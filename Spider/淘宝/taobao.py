# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-06 11:03:18
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-06 14:48:03

import sys
import io
import pymongo
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options) 
wait = WebDriverWait(browser, 15)
KEYWORD = 'iPad'
MONGO_URL = "localhost"
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
MAX_PAGE = 100


def index_page(page):
    """
    抓取索引页
    :param page:页码
    """
    print("正在爬取第", page, "页")
    try:
        url = "https://s.taobao.com/search?q="+quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input_content = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#mainsrp-pager div.form > input")))
            submit = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#mainsrp-pager div.form > sapn.btn.J_Submit")))
            input_content.clear()
            input_content.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#mainsrp-pager li.item.activate > span"), str(page)))
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException as e:
        print(e.msg)
        index_page(page)


def get_products():
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            "image": item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').test(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    """
    保存至MongoDB
    :param result:结果
    """
    try:
        if db[MONGO_COLLECTION].insert_one(result):
            print("存储到MongoDB成功")
    except Exception as e:
        print(e.args, "保存到MongoDB失败", sep=":")


def driver():
    for i in range(1, MAX_PAGE+1):
        index_page(i)


if __name__=="__main__":
    driver()
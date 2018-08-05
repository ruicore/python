# -*- coding: utf-8 -*-
# @Date:  2018-08-04 15:19:29
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-05 11:45:51

import time
import io
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

options=webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
# broswer = webdriver.Chrome(chrome_options=options)
broswer = webdriver.Chrome()
# broswer = webdriver.Firefox()
# broswer = webdriver.Edge()
# broswer = webdriver.PhantomJS()
# broswer = webdriver.Safari()
try:
    # broswer.get('https://www.baidu.com')
    # input = broswer.find_element_by_id('kw')
    # input.send_keys('Python')
    # input.send_keys(Keys.ENTER)
    # wait = WebDriverWait(broswer,10)
    # wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    # print(broswer.current_url)
    # print(broswer.get_cookies())
    # print(broswer.page_source)

    # broswer.get("https://www.taobao.com")
    # time.sleep(10)
    # input_first = broswer.find_element_by_id('q')
    # input_second = broswer.find_element_by_css_selector('#q')
    # input_third = broswer.find_element_by_xpath('//*[@id="q"]')
    # input_forth = broswer.find_element(By.ID,'q')
    # print(input_forth)
    # print(input_first,input_second,input_third)

    # broswer.get("https://www.taobao.com")
    # lis = broswer.find_elements_by_css_selector('.service-bd li')
    # print(lis)

    # broswer.get('https://www.taobao.com')
    # input_content = broswer.find_element_by_id('q')
    # input_content.send_keys('iphone')
    # time.sleep(1)
    # input_content.clear()
    # input_content.send_keys("iPad")
    # butten = broswer.find_element_by_class_name('btn-search')
    # butten.click()

    # url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    # broswer.get(url)
    # broswer.switch_to_frame("iframeResult")
    # source = broswer.find_element_by_css_selector("#draggable")
    # target = broswer.find_element_by_css_selector("#droppable")
    # actions = ActionChains(broswer)
    # actions.drag_and_drop(source,target)
    # actions.perform()
    # time.sleep(10)

    # broswer.get('https://www.zhihu.com/explore')
    # broswer.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # broswer.execute_script('alert("To Bottom")')
    # time.sleep(10)

    # url = 'https://www.zhihu.com/explore'
    # broswer.get(url)
    # logo = broswer.find_element_by_id('zh-top-link-logo')
    # print(logo)
    # print(logo.get_attribute('class'))
    # input_content = broswer.find_element_by_class_name('zu-top-add-question')
    # print(input_content.text)

    # url = 'https://www.zhihu.com/explore'
    # broswer.get(url)
    # input_content = broswer.find_element_by_class_name('zu-top-add-question')
    # print(input_content.id)
    # print(input_content.location)
    # print(input_content.tag_name)
    # print(input_content.size)

    # url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    # broswer.get(url)
    # broswer.switch_to_frame('iframeResult')
    # try:
    #     logo = broswer.find_element_by_class_name('logo')
    # except NoSuchElementException as e:
    #     print(e.msg)
    # broswer.switch_to.parent_frame()
    # logo = broswer.find_element_by_class_name('logo')
    # print(logo)
    # print(logo.text)

    # 显示的控制最长的等待时间
    # broswer.get('https://www.taobao.com')
    # wait = WebDriverWait(broswer,10)# 10 seconds
    # input_content = wait.until(EC.presence_of_element_located((By.ID,'q')))
    # button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-search')))
    # print(input_content,button)

    # broswer.get('https://www.baidu.com/')
    # broswer.get('https://www.taobao.com/')
    # broswer.get('https://www.python.org/')
    # broswer.back()
    # time.sleep(3)
    # broswer.forward()
    # time.sleep(3)
    # broswer.close()

    # broswer.get('https://www.zhihu.com/explore')
    # print(broswer.get_cookies())
    # broswer.add_cookie({"name":'name','domain':'www.zhihu.com','value':'germey'})
    # print(broswer.get_cookies())
    # broswer.delete_all_cookies()
    # print(broswer.get_cookies())

    # 多个选项卡
    broswer.get('https://www.baidu.com')
    broswer.execute_script('window.open()')
    print(broswer.window_handles)
    broswer.switch_to_window(broswer.window_handles[1])
    broswer.get('https://www.taobao.com')
    time.sleep(3)
    broswer.switch_to_window(broswer.window_handles[0])
    broswer.get('https://python.org')
finally:
    broswer.close()

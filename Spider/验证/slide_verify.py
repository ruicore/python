# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-10 10:48:37
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-10 10:49:23

import json
import webbrowser
import selenium
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

with open('secret.json') as f:
    secret = f.readlines()[0]
EMAIL = json.loads(secret).get('EMAIL')
PASSWORD = json.loads(secret).get('PASSWORD')
BORDER = 6
INIT_LEFT = 60


class CreackGeetest():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return: 按钮对象
        """
        button = self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_position(self):
        """
        获取验证码位置
        :return:验证码位置元祖
        """
        img = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, botton, left, right = location['y'], location['y'] + \
            size['height'], location['x'], location['x']+size['width']
        return (top, botton, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return:截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return：滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return:图片对象
        """
        top, bottom, left, right = self.get_position()
        print("验证码位置", top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha

    def __open(self):
        """打开网页输入用户密码
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(
            EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(
            EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1:图片1
        :param image2:图片2
        :param x:位置x
        :param y:位置y
        :return: 像素是否相同
        """
        # 去两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0]-pixel2[0] < threshold):
            if abs(pixel1[1]-pixel2[1] < threshold):
                if abs(pixel1[2]-pixel2[2] < threshold):
                    return True
        return False

    def get_gap(self, iamge1, image2):
        """
        获取缺口偏移量
        :param image1:不带缺口图片
        :param image2:带缺口图片
        :return:
        """
        left = 60
        for i in range(left, iamge1.size[0]):
            for j in range(iamge1.size[1]):
                if not self.is_pixel_equal(iamge1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance:偏移量
        :return:移动轨迹
        """
        # 移动轨迹
        track = []
        current = 0
        # 减速阈值
        mid = distance*4/5
        # 计算间隔
        t = 0.2
        v = 0
        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度为v0
            v0 = v
            # 当前速度v = v0+at
            v = v0 + a * t
            # 当前移动距离为：x =v0t+1/2*a*t**2
            move = v0*t+1/2*a*t*t
            # 当前位移
            current += move
            # 加速轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tarck):
        """
        拖动滑块到缺口处
        :param slider:滑块
        :param tarck:轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tarck:
            ActionChains(self.browser).move_by_offset(
                xoffset=x, yoffset=0).perform()
        time.sleep(5)
        ActionChains(self.browser).release().perform()

    def login(self):
        """
        登陆
        :return：None
        """
        submit = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        time.sleep(10)
        print("登陆成功")

    def crack(self):
        # 输入用户名
        self.__open()
        # 点击按钮
        button = self.get_geetest_button()
        button.click()
        # 获取验证码图片
        image1 = self.get_geetest_image('captcha1.png')
        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()
        # 获取带有缺口验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print("缺口位置", gap)
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print("滑动轨迹", track)
        # 拖动滑块
        self.move_to_gap(slider, track)
        sucess = self.wait.until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        print(sucess)
        # 失败后重试
        if not sucess:
            self.crack()
        else:
            self.login()


if __name__ == "__main__":
    crack = CreackGeetest()
    crack.crack()

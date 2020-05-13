#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   videosCrawler  
@Time        :   2020/5/13 11:46 上午
@Author      :   Xuesong Chen
@Description :   
"""
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

import random
from contextlib import closing



if __name__ == '__main__':

    start_url = 'https://cloud.tsinghua.edu.cn/d/9ee6160f580344749cf6/'

    # chromedriver的路径
    chromedriver = '/Users/cxs/libraries/chromedriver'
    # chromedriver = '/work/czm/driver/chromedriver'
    os.environ["webdriver.chrome.driver"] = chromedriver
    # 设置chrome开启的模式，headless就是无界面模式
    # 一定要使用这个模式，不然截不了全页面，只能截到你电脑的高度
    chrome_options = Options()
    # chrome_options.add_argument("--proxy-server=http://202.20.16.82:10152")
    # chrome_options.add_argument('headless')
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    driver.implicitly_wait(30)  # 隐性等待，最长等30秒

    driver.get(start_url)
    time.sleep(2 + 3*random.random())

    input_box = driver.find_element_by_class_name('input')
    input_box.send_keys('algoshare')
    driver.find_element_by_xpath("//*[@type='submit']").click()

    # html = driver.page_source.encode("utf-8", "ignore")

    course_elements = driver.find_elements_by_partial_link_text('讲')

    for idx in range(len(course_elements)):
        element = course_elements[idx]
        current_url = element.get_attribute('href')
        dir_name = element.text
        if dir_name not in ['第一讲', '第二讲', '第三讲', '第四讲']:
            continue
        if os.path.exists(dir_name):
            pass
        else:
            os.makedirs(dir_name)
        driver.get(current_url)
        videos_elements = driver.find_elements_by_partial_link_text('mp4')

        for video_idx in range(len(videos_elements)):
            video_element = videos_elements[video_idx]
            try:
                video_html = video_element.get_attribute('href')
                filepath = dir_name + '/' + video_element.text
                if os.path.exists(filepath):
                    continue
                driver.get(video_html)
                video_url = driver.find_element_by_class_name('vjs-tech').get_attribute('src')
                with closing(requests.get(video_url, stream=True)) as response:
                    chunk_size = 1024  # 单次请求最大值
                    content_size = int(response.headers['content-length'])  # 内容体总大小
                    data_count = 0
                    with open(filepath, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            data_count = data_count + len(data)
                            now_jd = (data_count / content_size) * 100
                            print("\r 文件下载进度：%d%%(%d/%d)" % (now_jd, data_count, content_size), end=" ")
            except:
                continue
            driver.back()
            videos_elements = driver.find_elements_by_partial_link_text('mp4')
        driver.back()
        driver.find_elements_by_partial_link_text('讲')

    driver.quit()




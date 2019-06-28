"""
作者：倪媛
功能：定义driver
日期：19/4/2019
"""

from selenium import webdriver
import os

# 无界面运行模式
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)

default_directory_rel = '../run_entrance/down_file/'
default_directory_abs = os.path.abspath(default_directory_rel)

prefs = {'download.default_directory': default_directory_abs}
chrome_options.add_experimental_option('prefs', prefs)


# 初始化driver
# driver = webdriver.Chrome()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(40)   # 隐性等待，最长等20秒
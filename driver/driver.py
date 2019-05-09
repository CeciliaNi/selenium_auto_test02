"""
作者：倪媛
功能：定义driver
日期：19/4/2019
"""

from selenium import webdriver

# 初始化driver
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(40)   # 隐性等待，最长等20秒
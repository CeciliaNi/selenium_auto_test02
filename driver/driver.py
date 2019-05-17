"""
作者：倪媛
功能：定义driver
日期：19/4/2019
"""

from selenium import webdriver


# 无界面运行模式
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)

# 初始化driver
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(40)   # 隐性等待，最长等20秒
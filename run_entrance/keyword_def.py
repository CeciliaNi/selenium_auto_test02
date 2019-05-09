"""
作者：倪媛
功能：根据关键字来定义页面操作的函数
日期：19/4/2019
"""

from driver.driver import driver
from selenium.webdriver.common.action_chains import ActionChains
import time


def key_word_func(keyword, type, loc, checkpoint=None, value=None, sleep_time=None):
    """
    根据关键字来定义页面元素操作方法
    :return:
    """
    try:
        if keyword == 'input':
            if type == 'xpath':
                driver.find_element_by_xpath(loc).send_keys(value)
            elif type == 'id':
                driver.find_element_by_id(loc).send_keys(value)
        elif keyword == 'click':
            if type == 'xpath':
                driver.find_element_by_xpath(loc).click()
        elif keyword == 'actionchains_click':
            if type == 'xpath':
                ActionChains(driver).click(driver.find_element_by_xpath(loc)).perform()
        elif keyword == 'assert':  # 断言
            for checktype, checkvalue in checkpoint.items():
                if type == 'xpath':
                    if checktype == 'len':
                        length = len(driver.find_elements_by_xpath(loc))
                        if length == checkvalue:
                            return True
                        else:
                            return False
                    elif checktype == 'text':
                        element_value = driver.find_element_by_xpath(loc).text.strip()
                        if element_value == checkvalue:
                            return True
                        else:
                            return False

        if sleep_time:
            time.sleep(sleep_time)

        return True

    except Exception as e:
        print(e)
        return False

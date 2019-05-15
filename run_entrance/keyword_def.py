"""
作者：倪媛
功能：根据关键字来定义页面操作的函数
日期：19/4/2019
"""

from driver.driver import driver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

long = 40
mid = 15
l_short = 10
short = 5
s_short = 2


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
        elif keyword == 'highlight':  # 元素定位，加红色边框
            if type == 'xpath':
                element = driver.find_element_by_xpath(loc)
                driver.execute_script(
                    "arguments[0].setAttribute('style', arguments[1]);", element,
                    "border: 2px solid red;"  # 边框border:2px; red红色
                )
        elif keyword == 'document_get':
            if type == 'className':
                js = "var q=document.getElementsByClassName" + loc + ".click()"
                driver.execute_script(js)
        elif keyword == 'until_wait':
            WebDriverWait(driver, 40, 0.5).until(
                EC.presence_of_element_located((By.XPATH, loc))
            )
        # elif keyword == 'until_not_wait':
        #     WebDriverWait(driver, 40, 0.5).until_not(
        #         EC.presence_of_element_located((By.XPATH, loc))
        #     )
        elif keyword == 'until_wait_click':
            WebDriverWait(driver, 40, 0.5).until(
                EC.presence_of_element_located((By.XPATH, loc))
            ).click()
        elif keyword == 'until_wait_actclick':
            WebDriverWait(driver, 40, 0.5).until(
                EC.presence_of_element_located((By.XPATH, loc))
            )
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
            if sleep_time == 'long':
                time.sleep(long)
            elif sleep_time == 'mid':
                time.sleep(mid)
            elif sleep_time == 'short':
                time.sleep(short)
            elif sleep_time == 's_short':
                time.sleep(s_short)
            else:
                time.sleep(sleep_time)

        return True

    except Exception as e:
        print(e)
        return False

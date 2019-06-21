"""
作者：倪媛
功能：根据关键字来定义页面操作的函数
日期：19/4/2019
"""
from driver.driver import driver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


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
        elif keyword == 'move_to':
            if type == 'xpath':
                ele = driver.find_element_by_xpath(loc)
                ActionChains(driver).move_to_element(ele).perform()
        elif keyword == 'vis_sel':
            if type == "id":
                s = driver.find_element_by_id(loc)
                Select(s).select_by_visible_text(value)
            elif type == 'xpath':
                s = driver.find_element_by_xpath(loc)
                Select(s).select_by_visible_text(value)
        elif keyword == 'actionchains_click':
            if type == 'xpath':
                 ActionChains(driver).click(driver.find_element_by_xpath(loc)).perform()
        elif keyword == 'actionchains_context_click':
            if type == 'xpath':
                ActionChains(driver).context_click(driver.find_element_by_xpath(loc)).perform()
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
            elif type == 'id':
                js = "var q=document.getElementById" + loc + ".click()"
            driver.execute_script(js)
        elif keyword == 'doc_get_len':
            if type == 'className':
                js_len = "return document.getElementsByClassName" + loc + ".length"
                len_num = driver.execute_script(js_len)
                js_exc = "document.getElementsByClassName" + loc + "["+str(len_num-1)+"].click()"
                driver.execute_script(js_exc)

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
            WebDriverWait(driver, 40, 1).until(
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
                else:
                     if checktype == 'file':
                        file_path = './down_file/'+checkvalue
                        time.sleep(3)
                        is_exists = os.path.exists(file_path)
                        if is_exists:
                            os.remove(file_path)
                            return True
                        else:
                            return False
        elif keyword == 'upload_file':
            # 上传文件
            file_name = value
            file_path = r'..\data\\' + file_name
            # 将上传文件的相对路径转换成绝对路径
            file_path = os.path.abspath(file_path)
            os.system("..\\data\\upload.exe %s" % file_path)  # 你自己本地的.exe路径
            time.sleep(3)
        elif keyword == 'minimize_window':
            driver.minimize_window()
        elif keyword == 'maximize_window':
            driver.maximize_window()
        elif keyword == 'switch_to':
            # 新网页为句柄1 移动到打开的网页
            latest_window = driver.window_handles[-1]
            driver.close()  # 关闭窗口，保证浏览器只有一个窗口
            driver.switch_to.window(latest_window)
            # windows = driver.window_handles
            # driver.switch_to.window(windows[-1])
        elif keyword == 'switch_iframe':
            if type == 'id':
                driver.switch_to.frame(driver.find_element_by_id(loc))
        elif keyword == 'switch_iframe_out':
            driver.switch_to_default_content()
        if sleep_time:
            time.sleep(sleep_time)
        else:
            time.sleep(1)
        return True

    except Exception as e:
        print(e)
        return False

"""
    作者：倪媛
    功能：截图保存操作
    日期：16/4/2019
"""
import time
import os
from driver.driver import driver

base_path = '../picture/results/'


def save_img(test_suite_name):
    """
    截图保存
    """
    date_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    hour_time = time.strftime("%H_%M_%S", time.localtime(time.time()))

    path = base_path + '/' + date_time
    # 判断路径是否存在
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
    pic_path = path + '/' + test_suite_name + '_' + hour_time + '.png'
    # 这里注意save_screenshot()填入的路径必须是已有的文件夹路径，所以之前要进行路径判断后没有新建
    # driver.save_screenshot(pic_path)
    driver.get_screenshot_as_file(pic_path)

    return pic_path

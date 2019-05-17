"""
作者：倪媛
功能：运行测试用例 生成html报告
日期：29/4/2019
"""

import unittest
from report import HTMLTestReportCN
import os
import time
from driver.driver import driver


report_path = '../report/'
case_path = '../run_entrance/'


def add_case(casepath=case_path, rule="test_api_cnj*.py"):
    """
    加载所有的测试文件
    :return:
    """
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(casepath, pattern=rule)

    return discover


def run_case(all_case, reportpath=report_path):
    """
    执行所有的用例, 并把结果写入测试报告
    :return:
    """
    # html报告显示为'result_2019-05-16.html'这样的格式
    date_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    htmlreport_path = reportpath + 'result_' + date_time + '.html'

    # 报告文件的相对路径转绝对路径
    abs_htmlreport_path = os.path.abspath(htmlreport_path)

    print('测试报告生成地址：{}'.format(abs_htmlreport_path))
    fp = open(htmlreport_path, 'wb')
    runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, verbosity=2, title='测试报告', description='用例执行情况')
    runner.run(all_case)
    fp.close()


if __name__ == '__main__':
    cases = add_case()
    run_case(cases)
    driver.quit()
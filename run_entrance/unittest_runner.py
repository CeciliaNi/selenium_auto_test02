"""
作者：倪媛
功能：运行测试用例 生成html报告
日期：29/4/2019
"""
import sys
import os
# 当前项目路径加入到环境变量中，让解析器能找到第一model的目录
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

import unittest
from report import HTMLTestReportCN
import time
from driver.driver import driver
import glob
from shutil import copyfile
import shutil


date_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
report_scan_path = '../report/'
case_path = '../run_entrance/'
suite_path = '../run_entrance/test_suite/'
pic_base_path = '../picture/results/' + date_time
report_base_path = '../report/' + date_time

# 判断截图路径是否存在
is_pic_exists = os.path.exists(pic_base_path)
if is_pic_exists:
    # 先强制删除文件夹，再重新建同名文件夹即可
    shutil.rmtree(pic_base_path)
    os.makedirs(pic_base_path)

# 判断报告文件路径是否存在
is_rpt_exists = os.path.exists(report_base_path)
if is_rpt_exists:
    # 先强制删除文件夹，再重新建同名文件夹即可
    shutil.rmtree(report_base_path)
    os.makedirs(report_base_path)


# 扫描测试文档的设定
rule_excl = '*'
if rule_excl == '*':
    rule_config = "test_api_*.py"
    excel_file = 'test_suite_*'
else:
    rule_config = "test_api_"+rule_excl+"*.py"
    excel_file = 'test_suite_'+rule_excl+'*.xlsx'
# 测试用例的扫描路径
suite_excute_path = suite_path + excel_file
# 扫描出目标测试用例列表
file_list = glob.glob(suite_excute_path)  # ['C:\\Users\\wangwenbo\\selenium_auto_test02\\run_entrance\\test_suite\\test_suite_cnj01接件.xlsx']
# 针对每个测试用例文件复制出测试py文件
py_file_list = []
for each_file in file_list:
    file_full_name = each_file.split("\\")[-1]  # test_suite_cnj01接件.xlsx
    file_name = file_full_name[:file_full_name.rfind(".")]  # test_suite_cnj01接件
    sub_name = file_name.split("_")[-1]  # cnj01接件
    py_file = 'test_api_'+sub_name+'.py'
    # 复制出test_api的py文件
    copyfile('test_template.py', py_file)
    py_file_list.append(py_file)


def add_case(casepath=case_path, rule=rule_config):
    """
    加载所有的测试文件
    :return:
    """
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(casepath, pattern=rule)

    return discover


def run_case(all_case, reportpath=report_scan_path):
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


def report_file_del():
    # date_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    pic_path = pic_base_path + '/*.png'
    # 扫描出当天图片截图列表
    pic_list = glob.glob(pic_path)
    suite_set = set()  # 创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
    for pic_file in pic_list:
        pic_full_name = pic_file.split("\\")[-1]
        pic_name = pic_full_name[:pic_full_name.rfind(".")]
        pic_suite_name = pic_name.split("_")[0]
        suite_set.add(pic_suite_name)

    # 扫描出当天报告列表
    report_path = report_base_path + '/*.xlsx'
    rpt_list = glob.glob(report_path)
    for rpt_file in rpt_list:
        rpt_full_name = rpt_file.split("\\")[-1]
        rpt_name = rpt_full_name[:rpt_full_name.rfind(".")]
        rpt_suite_name = rpt_name.split("_")[-1]
        # 如果报告文件不在截图文件列表中，则表明该模块没有报错，删除该报告文件
        if not rpt_suite_name in suite_set:
            os.remove(rpt_file)


if __name__ == '__main__':
    cases = add_case()
    run_case(cases)
    driver.quit()
    # 删除py文件
    for each_file in py_file_list:
        os.remove(each_file)
    # 对报告文件进行整合，如果没有报错就删除，只保留有报错模块的报告文件
    report_file_del()

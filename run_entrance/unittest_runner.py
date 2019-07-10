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
import datetime
from driver.driver import driver
import glob
from shutil import copyfile
import shutil


date_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
report_scan_path = '../report/'
case_path = '../run_entrance/'
suite_path = '../run_entrance/test_suite/'
pic_base_path = '../picture/results/' + date_time
report_base_path = '../report/report_excel/' + date_time

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


def save_five_day_file():
    # 由今天的日期推算出5天前的日期
    today_date =datetime.datetime.now().date()
    five_days_ago = today_date + datetime.timedelta(days=-4)

    # 获取results目录下的所有文件夹名称列表
    results_path = r'../picture/results'
    pic_folder_str_list = os.listdir(results_path)
    # 删除5天前的截图文件夹
    for pic_folder_str in pic_folder_str_list:
        folder_name_list = pic_folder_str.split('-')
        year = int(folder_name_list[0])
        month = int(folder_name_list[1])
        day = int(folder_name_list[2])
        folder_date = datetime.date(year, month, day)
        # 进行判断 如果是5天前的则删除
        if folder_date < five_days_ago:
            folder_path = '../picture/results/' + pic_folder_str
            shutil.rmtree(folder_path)

    # 获取report目录下的所有文件夹名称列表
    rpt_path = r'../report/report_excel'
    rpt_folder_str_list = os.listdir(rpt_path)
    # 删除5天前的excel报告文件夹
    for rpt_folder_str in rpt_folder_str_list:
        folder_name_list = rpt_folder_str.split('-')
        year = int(folder_name_list[0])
        month = int(folder_name_list[1])
        day = int(folder_name_list[2])
        folder_date = datetime.date(year, month, day)
        # 进行判断 如果是5天前的则删除
        if folder_date < five_days_ago:
            folder_path = '../report/report_excel/' + rpt_folder_str
            shutil.rmtree(folder_path)

    # 扫描出所有html报告文件
    html_rpt_path = report_scan_path + '\*.html'
    html_rpt_list = glob.glob(html_rpt_path)
    for html_rpt in html_rpt_list:
        html_full_name = html_rpt.split("\\")[-1]
        html_name = html_full_name[:html_full_name.rfind(".")]
        html_name_list = html_name.split("_")
        year = int(html_name_list[1].split('-')[0])
        month = int(html_name_list[1].split('-')[1])
        day = int(html_name_list[1].split('-')[2])
        html_date = datetime.date(year, month, day)
        # 如果该html文件是5天前的则删除
        if html_date < five_days_ago:
            html_file_path = '../report/' + html_rpt
            os.remove(html_file_path)


if __name__ == '__main__':
    cases = add_case()
    run_case(cases)
    driver.quit()
    # 删除py文件
    for each_file in py_file_list:
        os.remove(each_file)
    # 对报告文件进行整合，如果没有报错就删除，只保留有报错模块的报告文件
    report_file_del()

    # 对报告文件及截图文件夹只保留近5天的数据
    save_five_day_file()

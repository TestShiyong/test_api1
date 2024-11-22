#:@ TIME 2021/11/14   17:32
#:@FILE  test_ywl.py
#:@EMAIL  1557225637@QQ.COM
# 导入模块
import unittest
from ddt import ddt, data
from common.handleData import Global_var, clearGlobalVar
from common.handleExcel import Excel_data
from common.handleData import extract, replaceAllData
from common.handleLog import new_log
from common.handleNewEmail import newEmai
from common.handleRequest import sendRequest
import path

# 创建ddt对象
new_case = Excel_data(path.excel_dir + r'\excel_data.xlsx', 'ywls')
cases = new_case.allData()


# 创建测试类
# 引入ddt
@ddt()
class Ywl(unittest.TestCase):
    # 前置条件
    @classmethod
    def setUpClass(cls) -> None:
        new_log.info("======    加车用例开始      ======")
        email = newEmai()
        setattr(Global_var, 'email', email)

    # 后置条件
    @classmethod
    def tearDownClass(cls) -> None:
        new_log.info("======    加车用例结束      ======")
        clearGlobalVar()
        new_case.close_excel()

    # 用例方法
    # 导入excel参数
    @data(*cases)
    def test_ywl(self, case): \
            # 替换数据
        case = replaceAllData(case)
        # if sql
        # if token
        # 调用接口
        if hasattr(Global_var, 'token'):
            res = sendRequest(case['method'], case['url'], case['data'], token=Global_var.token)
        else:
            res = sendRequest(case['method'], case['url'], case['data'])
        # if 提取数据
        if case['extract_data']:
            extract(case['extract_data'], res.json())

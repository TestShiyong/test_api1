#:@ TIME 2021/11/14   17:32
#:@FILE  test_ywl.py
#:@EMAIL  1557225637@QQ.COM
# 导入模块
import unittest
from ddt import ddt, data
from common.handle_data import Global_var, Clear_global_var
from common.handle_excel import Excel_data
from common.handle_data import extract, replace_all_data
from common.handle_log import new_log
from common.handle_new_email import get_new_emai
from common.handle_request import send_request
import path

# 创建ddt对象
new_case = Excel_data(path.excel_dir + r'\excel_data.xlsx', 'ywls')
cases = new_case.all_data()


# 创建测试类
# 引入ddt
@ddt()
class Ywl(unittest.TestCase):
    # 前置条件
    @classmethod
    def setUpClass(cls) -> None:
        new_log.info("======    加车用例开始      ======")
        email = get_new_emai()
        setattr(Global_var, 'email', email)

    # 后置条件
    @classmethod
    def tearDownClass(cls) -> None:
        new_log.info("======    加车用例结束      ======")
        Clear_global_var()
        new_case.close_excel()

    # 用例方法
    # 导入excel参数
    @data(*cases)
    def test_ywl(self, case): \
            # 替换数据
        case = replace_all_data(case)
        # if sql
        # if token
        # 调用接口
        if hasattr(Global_var, 'token'):
            res = send_request(case['method'], case['url'], case['data'], token=Global_var.token)
        else:
            res = send_request(case['method'], case['url'], case['data'])
        # if 提取数据
        if case['extract_data']:
            extract(case['extract_data'], res.json())

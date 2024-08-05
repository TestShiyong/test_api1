
#:@ TIME 2021/10/3   13:13
#:@FILE  test_register.py
#:@EMAIL  1557225637@QQ.COM
import unittest
from ddt import ddt,data
import path
import json
import random
from common.handle_log import new_log
from common.handle_excel import Excel_data
from common.handle_data import Global_var,replace_all_data
from common.handle_database import Database
from common.handle_request import send_request

new_register_data = Excel_data(path.excel_dir + '\\excel_data.xlsx', 'register')  # 创建ddt对象
db = Database()

@ddt()
class Test_register(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        new_log.info("======  注册模块用例 开始执行  ========")

    @classmethod
    def tearDownClass(cls) -> None:
        new_log.info("====== 注册模块用例 执行结束  ========")
        db.close_db()

    # #注册成功
    @data(*new_register_data.all_data())
    def test_register(self,case):
        self._testMethodDoc = case['case_name']
        new_log.info("*********   执行用例{}：{}   *********".format(case["id"],case["case_name"]))
        #
        if case['data'].find("#email#")!=1:
            new_email=''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8))
            setattr(Global_var,'email',new_email)
            case=replace_all_data(case)

        # 步骤 测试数据 - 发起请求
        res = send_request('post',case['url'],case['data'])

        # 期望结果，从字符串转换成字典对象
        expect=eval(case['expect'])
        try:
            self.assertEqual(res.json().get('code'),expect['code'])
            self.assertEqual(res.json()['msg'],expect['msg'])
            if case['check_sql']:
                new_log.debug('需要校验数据库')
        except AssertionError:
            new_log.debug("断言失败............................断言失败",AssertionError)
            raise


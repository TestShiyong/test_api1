
#:@ TIME 2021/10/3   13:13
#:@FILE  testRegister.py
#:@EMAIL  1557225637@QQ.COM
import unittest
from ddt import ddt,data
import path
import json
import random
from common.handleLog import log
from common.handleExcel import Excel
from common.handleData import GlobalData,replaceAllData,GlobalData
from common.handleDatabase import Database
from common.handleRequest import sendRequest

new_register_data = Excel(path.excel_dir + '\\Excel.xlsx', 'register')  # 创建ddt对象
db = Database()

@ddt()
class Test_register(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        log.info("======  注册模块用例 开始执行  ========")

    @classmethod
    def tearDownClass(cls) -> None:
        log.info("====== 注册模块用例 执行结束  ========")
        db.close_db()

    # #注册成功
    @data(*new_register_data.allData())
    def test_register(self,case):
        self._testMethodDoc = case['case_name']
        log.info("*********   执行用例{}：{}   *********".format(case["id"],case["case_name"]))
        #
        if case['data'].find("#email#")!=1:
            new_email=''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8))
            setattr(GlobalData,'email',new_email)
            case=replaceAllData(case)

        # 步骤 测试数据 - 发起请求
        res = sendRequest('post', case['url'], case['data'])

        # 期望结果，从字符串转换成字典对象
        expect=eval(case['expect'])
        try:
            self.assertEqual(res.json().get('code'),expect['code'])
            self.assertEqual(res.json()['msg'],expect['msg'])
            if case['check_sql']:
                log.debug('需要校验数据库')
        except AssertionError:
            log.debug("断言失败............................断言失败",AssertionError)
            raise


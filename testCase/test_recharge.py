#:@ TIME 2021/10/28   1:17
#:@FILE  test_recharge.py
#:@EMAIL  1557225637@QQ.COM
# from api.recharge import Recharge
from common.handleExcel import Excel
from common.handleLog import new_log
from common.handleDatabase import Database
from common.handleData import replaceData
from common.handleData import replaceAllData
from ddt import ddt, data
import json
import path
import unittest

new_ddt = Excel(path.excel_dir + '\\excel_data.xlsx', 'recharge')  # 创建ddt对象


@ddt()
class Test_recharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        new_log.info("======  充值模块用例 开始执行  ========")
        cls.new_recharge = Recharge()
        # cls.email,cls.password=cf.get_str('Account','email'),cf.get_str('Account','password')
        cls.db = Database()

    @classmethod
    def tearDownClass(cls) -> None:
        new_log.info("======  充值模块用例 执行结束  ========")

    @data(*new_ddt.allData())
    def test_recharges(self, case):
        self._testMethodDoc = case['case_name']
        if case['check_sq']:
            case = replaceAllData(case)
            db_money = float(self.db.getFetchone(case['check_sq'])['MONEY'])  # 查询数据库当前余额
            new_log.debug('当前数据库余额：{}'.format(db_money))
            add_money = float(json.loads(case['data'])['money'])  # 获取用例增加的额度
            sum_money = db_money + add_money  # 获取sum额度
            # 更新期望额度
            case = replaceData(case, str(sum_money), '#new_money#')  # 替换sum额度
        # 发起请求 进行充值
        response = self.new_recharge.recharge(json.loads(case['data']))

        new_log.debug('测试用例：{}'.format(case['case_name']))
        new_log.debug('替换后的case：{}'.format(case))
        new_log.debug('接口响应参数:{}'.format(response.json()))

        # 将期望结果转成字段 再去对比

        self.assertEqual(json.loads(case['expect'])['code'], response.json()['code'])
        self.assertEqual(json.loads(case['expect'])['msg'], response.json()['msg'])
        if case['check_sq']:
            self.assertEqual(json.loads(case['expect'])['money'], str(response.json()['money']))

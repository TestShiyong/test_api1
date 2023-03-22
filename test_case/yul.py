#:@ TIME 2021/12/17   12:47
#:@FILE  yul.py
#:@EMAIL  1557225637@QQ.COM
import unittest
from api.login import LoginAPI
from common.handle_cf_file import new_cfFile as cf
from common.handle_request import get_headers


import requests
class Test_add_cart(unittest.TestCase):

    def setUp(self) -> None:
        url='https://api-t-7.azazie.com/1.0/user/login'
        data={"email":"ys@tetx.com","password":"123456"}
        response=requests.post(url,json=data,headers=get_headers())
        token=response.json()['data']['token']
        self.token=token


    def tearDown(self) -> None:
        pass

    def  test_add_cart(self):
        url1='https://api-t-7.azazie.com/1.0/cart/goods'

        data={
        "act": "addGoodsToCart",
        "goods_id": 1002167,
        "dress_type": 'dress',
        "from_showroom": "",
        "from_whatAreU": "",
        "recommend_flag": "",
        "from_details_entry": "",
        "from_instagram": "",
        "styles": {
            "freeStyle": False, "size_type": "_inch",
            "select": {
                "color": 11629, "size":'wd2'
            }
        },
        "goods_number": 1
        }+
        +++
        .self++-
        res=requests.post(url1,data,get_headers(token=self.token))
        print('购物车返回参数:',res.json())


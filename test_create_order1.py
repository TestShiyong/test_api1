import base64
import json
import os

import requests


# 环境地址pip
env_url = "https://api-t-1.azazie.com/"
# env_url = "https://apix-p.azazie.com/"
country = "US"  # 站点   可修改CA
# country = "CA"
order_sn_list = "order_sn_list1.txt"   # 按照组合序号直接修改list后面的数字

# 账号信息
username, password = 'yzhang@qq.com', '12345678'
# username, password = 'orderautotest8@tetx.com', '123456'

# 循环次数
num = 10  # 修改循环次数

# 商品信息
address_id = 6228878
# shippingmethod_id = 24  #加急
shipping_method_id = 2
# payment_id = 97  # paypal
payment_id = 186  # credit

# bug_now字段base64 编码
goods = dict()
style = dict()
colorSize = dict()
goods['goods_id'] = 1000020  # 写入需要加车的goods_id
goods['act'] = 'addGoodsToCart'
goods['dress_type'] = 'dress'
goods['from_showroom'] = ''
goods['from_whatAreU'] = ''
goods['recommend_flag'] = ''
goods['from_details_entry'] = ''
goods['from_instagram'] = ''
goods['goods_number'] = 1
goods['styles'] = style
style['freeStyle'] = False
style['size_type'] = '_inch'
style['customName'] = ''
style['select'] = colorSize
colorSize['color'] = 529  # 需要加车的color_id
colorSize['size'] = 7494  # 需要加车的size_id

buy = json.dumps(goods)
buy = buy.replace(' ', '')
buy = buy.encode(encoding='utf-8')
buy.decode()
buy = base64.b64encode(buy)
buy_now = buy.decode()
print(buy_now)


# 红包信息
coupon_code = "forever6"

# 信用卡信息
card_number = "4514617632552453"
exp_date = '12/2021'
month = '12'
year = '2021'
card_code = '123'


def order_create_login_email():
    '''判断账号是否存在，不存在则创建'''
    check_email_register_uri = '1.0/user/email'
    check_data = {"email": f"{username}"}
    print(f"检测账户{username}是否已注册，pwd:{password}")
    res = requests.get(url=env_url + check_email_register_uri, json=check_data)
    if "Your email already exists." != res.json()["msg"]:
        register_uri = '1.0/user/register'
        register_data = {"email": f"{username}", "password": f"{password}", "wedding_date": ""}
        res = requests.post(url=env_url + register_uri, json=register_data)
        if "success" == res.json()["msg"]:
            print(f"用户{username}已成功注册")
    else:
        print(f"用户{username}已存在")


def order_login():
    '''用户登录'''
    order_create_login_email()
    login_uri = '1.0/user/login'
    login_data = {"email": f'{username}', "password": f'{password}'}

    print(f"{username}用户开始登录")
    res = requests.post(url=env_url + login_uri, json=login_data)
    print(f"用户登录，响应结果：{res.json()}")
    try:
        if res.json()["data"]["token"]:
            print(f"{username}用户已登录")
    except KeyError:
        print(f"{username}用户登录失败")
        token = None
    else:
        token = res.json()["data"]["token"]
    return token

def get_address_id(token, country):
    headers = {"Content-Type": "application/json", "x-token": f"{token}",
               "x-countryCode": country}
    if country == 'US':
        data = {"check_validation": 1, "address_type": 1, "first_name": "Ted", "last_name": "Cobra", "country": 3859,
                "province": 3871, "city_text": "HUNTINGTON BEACH", "address": "16701 BEACH BLVD", "sign_building": "",
                "zipcode": "92647-4814", "tel": "2345678910"}
    else:
        data = {"check_validation": 1, "address_type": 1, "first_name": "Ted", "last_name": "Cobra", "country": 3844,
                "province": 3845, "city_text": "HUNTINGTON BEACH", "address": "16701 BEACH BLVD", "sign_building": "",
                "zipcode": "92647-4814", "tel": "2345678910"}
    res = requests.post(url=env_url + '1.0/address/add', headers=headers, json=data)
    print(f"获取address信息，响应结果：{res.text}")
    if res.json()['code'] == 100501:
        return None
    address_id = res.json()['data']['addressList']['shippingAddress'][0]['addressId']
    # print(f"address_id：{address_id}")

    return address_id

def test_batch_order():
    """buy now 下单"""
    i = 1
    while i <= num:
        i += 1
        token = order_login()

        address_id = get_address_id(token=token, country=f'{country}')
        print(f"用户token：{token}")

        print(f"address_id：{address_id}")

        print(f"payment_id：{payment_id}")

        print(f"shipping_method_id：{shipping_method_id}")

        new_headers = {"Content-Type": "application/json", "x-app": "pc", "x-token": f"{token}", "x-project": "azazie", "x-countryCode": f"{country}"}  # 可修改pc/h5  选择us/ca站点
        print(new_headers)
    # paypal支付 未支付成功
    # data_paypal = {"order_sn": "", "payment_id": 97, "shipping_method_id": f"{shipping_method_id}", "address_id": f"{address_id}", "coupon_code": "forever6", "order_track_id": "{order_track_id}", "event_date": "", "card_number": "", "exp_date": "", "month": "", "year": "", "card_code": "", "dot_list": "VersionA_GuestCheckout"}
    #
    # actual_result1 = requests.post(url=conf_url.get_value("request", "url") + "1.0/order",
    #                                headers=new_headers,
    #                                json=data_paypal,
    #                                verify=False)
    #
    # case_logger.info(f"响应结果： {actual_result1.text}")

    # credit 支付 未支付成功
        data_cridet = {"sn": "", "payment_id": f"{payment_id}", "shipping_method_id": f"{shipping_method_id}",
                        "address_id": f"{address_id}", "coupon_code": f"{coupon_code}", "order_track_id": "", "event_date": "",
                       "card_number": f"{card_number}", "exp_date": f"{exp_date}", "month": f"{month}", "year": f'{year}', "card_code": f"{card_code}",
                       "order_dot": "", "order_type": "normal","origin_ordr_sn": "","rec_ids": "","buy_now":f"{buy_now}"}
        print(data_cridet)
        actual_result2 = requests.post(url=env_url + "1.0/order",
                                            headers=new_headers,
                                            json=data_cridet,
                                            verify=False)

        print(f"响应结果： {actual_result2.text}")
        if country == "US":
            order_sn = actual_result2.json()['data']['orderSn']
        else:
            order_sn = actual_result2.json()['data']['orderInfo']['orderSn']
        if os.path.isfile(f'{order_sn_list}') is False:
            f = open(f'{order_sn_list}', 'w')
            f.write(order_sn + '\r\n')
            f.close()
        else:
            f = open(f'{order_sn_list}', 'a')
            f.write(order_sn + '\r\n')
            f.close()


    print("循环结束")


if __name__ =="__main__":
    test_batch_order()
import requests
import time


def register():
    # 获取当前时间戳
    timestamp = int(time.time())

    # 将时间戳转换为指定格式的日期（不包含年份）
    date = time.strftime('%m%d%H%M', time.localtime(timestamp))

    url = 'https://ft1.azazie.com/test/1.0/user/register'
    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie'
    }

    data = {
        'email': f'test_shiyong{date}@gaoyaya.com',
        'name': f'test_shiyong{date}',
        'password': '123456',
        'is_check_email_suffix': '1',
        'categories[0]': 'page_common_new_user_category_bd'
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.json()['data']['email'])
    return response.json()['data']['token']


def login(email, password):
    url = 'https://api-t-7.azazie.com/1.0/user/login'
    data = {
        'email': email,
        'password': password
    }
    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie'
    }

    result = requests.post(url=url, json=data, headers=headers)
    login_token = result.json()['data']['token']
    return login_token


def addAddress(token):
    url = 'https://ft1.azazie.com/test/1.0/address/add'

    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie',
        'x-token': token
    }

    data = {
        "address_type": 1,
        "country": 3859,
        "province": 3871,
        "province_text": "California",
        "city": 385920049360,
        "city_text": "San Jose",
        "district": 0,
        "district_text": "",
        "address": "1234 Pine Street",
        "sign_building": "",
        "zipcode": "95112",
        "check_validation": 0,
        "first_name": "yong",
        "last_name": "shi",
        "tel": "1454745215",
        "order_country_code": "US",
        "sort_by": ""
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)


def addToCart(token, goods_id=1008051, goods_number=1, dress_type='dress', styles=None):
    url = 'https://ft1.azazie.com/test/1.0/cart/goods'

    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie',
        'x-token': token
    }
    data = {
        "act": "addGoodsToCart",
        "from_showroom": "",
        "from_details_entry": "",
        "from_instagram": "",
        "from_whatAreU": "",
        "recommend_flag": "",
        "goods_id": 1008051,
        "dress_type": "dress",
        "goods_number": 1,
        "styles": {
            "freeStyle": False,
            "size_type": "_inch",
            "select": {"color": 5714, "size": 7525},
            "customNameList": {"line1": ""}
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.text)

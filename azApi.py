import requests
import time

BASE_URL = 'https://api-t-2.azazie.com'

# BASE_URL = 'https://apix.azazie.com'
test_order_data_list = []


def register(email=None):
    timestamp = int(time.time())
    date = time.strftime('%m%d%H%M%S', time.localtime(timestamp))
    url = f'{BASE_URL}/1.0/user/register'
    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie',

    }

    if not email:
        email = f'test_shiyong{date}@gaoyaya.com'
    data = {
        'email': email,
        'name': email[:-12],
        'password': '123456',
        'is_check_email_suffix': '1',
        'categories[0]': 'page_common_new_user_category_bd'
    }
    response = requests.post(url, headers=headers, data=data)
    email = response.json()['data']['email']
    print('register()', email)
    global test_order_data_list
    test_order_data_list.append(email)
    return response.json()['data']['token']


def login(email, password):
    url = f'{BASE_URL}/1.0/user/login'
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
    res = result.json()
    login_token = result.json()['data']['token']
    print(result.json())
    return login_token


def createAddress(token):
    url = f'{BASE_URL}/1.0/address/add'

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
    print('createAddress()', response.json())
    address_list = response.json()['data']['addressList']['shippingAddress']
    return address_list[0]['addressId']


def getAddress(token):
    url = f'{BASE_URL}/1.0/address/get'
    headers = {
        'x-app': 'pc',
        'x-countrycode': 'us',
        'x-languagecode': 'en',
        'x-token': token,
    }

    response = requests.get(url, headers=headers)
    address_list = response.json()['data']['shippingAddress']
    if not address_list:
        addressId = createAddress(token)
        return addressId
    addressId = address_list[0]['addressId']
    print('getAddress():', addressId)
    return addressId


def addToCart(token, goods_id=1008051, goods_number=1, dress_type='dress', styles=None):
    url = f'{BASE_URL}/1.0/cart/goods'
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
        "goods_id": goods_id,
        "dress_type": dress_type,
        "goods_number": goods_number,
        "styles": {
            "freeStyle": False,
            "size_type": "_inch",
            "select": {"color": 5714, "size": 7525},
            "customNameList": {"line1": ""}
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print('addToCart()', response.json())


def createOrder(token, address_id):
    global test_order_data_list
    url = f'{BASE_URL}/1.0/order'
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-project': 'azazie',
        'x-token': token
    }
    data = {
        "order_sn": "",
        "payment_id": 186,
        "shipping_method_id": "2",
        "address_id": address_id,
        "coupon_code": "forever111",
        "use_account_balance": False,
        "order_track_id": "",
        "event_date": "",
        "order_type": "normal",
        "card_number": "4000000000001000",
        "exp_date": "01/2027",
        "month": "01",
        "year": "2027",
        "card_code": "116",
        "version": "a",
        "robot_validation":1
    }
    print(f'createOrder data: {data}')
    response = requests.post(url, headers=headers, json=data)
    print('createOrder()', response.json())
    order_sn = response.json()['data']['orderSn']
    test_order_data_list.append(order_sn)

    return order_sn


def payment(order_sn, token):
    import requests

    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie',
        'x-refer-request-trace-id': '',
        'x-request-trace-user-uid': '',
        'x-token': token
    }

    data = {
        "nonce": "",
        "order_sn": order_sn,
        "REF": "10111010",
        "device_id": 115408886,
        "use_account_balance": False
    }

    response = requests.post(f'{BASE_URL}/1.0/order/payment', headers=headers, json=data)

    print('payment', response.json())


if __name__ == '__main__':
    # token = register()
    token = login('shiyong@gaoyaya.com', '123456')
    print(token)
    address_id = getAddress(token)
    # addToCart(token, goods_number=1)
    order_sn = createOrder(token, address_id)
    payment(order_sn, token)
    pass

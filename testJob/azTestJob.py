import requests
from common.handleDatabase import Database

from datetime import datetime, timezone, timedelta
import time


def loginAZ(is_pro=None):
    url = 'https://api-t-1.azazie.com/1.0/user/login'
    if is_pro:
        url = 'https://apix.azazie.com/1.0/user/login'
    headers = {"Content-Type": "application/json", "x-app": 'pc', "x-token": "",
               "x-project": "azazie", "x-countryCode": 'us'}
    payload = {
        'email': 'shiyong@gaoyaya.com', 'password': 123456
    }
    try:
        result = requests.post(url, json=payload, headers=headers)
        token = result.json()['data']['token']
        return token
    except:
        print('login接口报错')


def getRecId(token):
    headers = {"Content-Type": "application/json", "x-app": 'pc', "x-token": token,
               "x-project": "azazie", "x-countryCode": 'us'}
    url = 'https://apix.azazie.com/1.0/cart'
    res = requests.get(url, headers=headers)
    checkout_goods_list = res.json()['data']['checkoutGoodsList']
    rec_id_list = []
    if checkout_goods_list:
        for item in checkout_goods_list:
            rec_id_list.append(item['recId'])
    print(rec_id_list)
    return rec_id_list


def deleteCard(rec_id_list, token, is_pro=None):
    headers = {"Content-Type": "application/json", "x-app": 'pc', "x-token": token,
               "x-project": "azazie", "x-countryCode": 'us'}
    for rec_id in rec_id_list:
        url = f'https://api-t-7.azazie.com/1.0/cart/goods/{rec_id}'
        if is_pro:
            url = f'https://apix.azazie.com/1.0/cart/goods/{rec_id}'
        res = requests.delete(url, headers=headers)
        print('deleteCard:', res.status_code)


def getOrderId(token):
    order_sn = ''
    order_detail_url = f'https://api-t-1.azazie.com/1.0/order/detail?order_sn={order_sn}'
    headers = {"Content-Type": "application/json", "x-app": 'pc', "x-token": token,
               "x-project": "azazie", "x-countryCode": 'us'}

    result = requests.get(url=order_detail_url, headers=headers)
    order_id = result.json()['data']['orderIds'][order_sn]
    return order_id


def group_list(l1):
    l2 = []
    for goods in l1:
        if goods not in l2:
            l2.append(goods)
    return l2


def detail_page_colors(goods_id):
    li = []
    header = {"Content-Type": "application/json",
              "Accept": "application/json",
              "x-app": "pc",
              "x-token": "",
              "x-project": "azazie",
              "x-countryCode": "US",
              "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
              }
    url = f'https://apix-p6.azazie.com/1.0/product/first-screen?goods_id={goods_id}'
    data = requests.get(url, headers=header).json()['data']['styleInfo']['color']
    try:
        for k, _ in data.items():
            li.append(k)
        return len(li)
    except Exception:
        print(f'数据异常 id:{goods_id}')


def group_goods(url, page_numbers, datas):
    """
    列表页接口返回数据 判断列表goods是否有重复
    :return:
    """
    header = {"Content-Type": "application/json",
              "Accept": "application/json",
              "x-app": "pc",
              "x-token": "",
              "x-project": "azazie",
              "x-countryCode": "US",
              "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
              }

    goods_list = []
    for number in range(*page_numbers):
        url_with_page = url.replace("page=1", f"page={number}")
        res = requests.post(url_with_page, json=datas, headers=header)
        dict1 = res.json()['data']['prodList']
        for item in dict1:
            goods_list.append(item['goodsId'])
    no_duplicates = group_list(goods_list)
    print(f"Total number of goods: {len(goods_list)}")
    print(goods_list)
    for item_id in no_duplicates:
        count_color_number = detail_page_colors(item_id)
        indexes_of_1 = [index for index, value in enumerate(goods_list) if value == item_id]
        print(f"Item ID: {item_id}, Count_goods: {goods_list.count(item_id)},count_color_number：{count_color_number}",
              indexes_of_1)
    return goods_list


def az_database():
    """
    AZ数据库获取数据 处理
    :return:
    """
    header = {"Content-Type": "application/json",
              "Accept": "application/json",
              "Connection": "keep-alive",
              "Host": "audit-az.gaoyaya.com",
              "Origin": "https://audit-az.gaoyaya.com",
              "Referer": "https://audit-az.gaoyaya.com/",
              "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTUzMjI1NTQsIm5hbWUiOiJzaGl5b25nIiwicm9sZSI6Imd1ZXN0In0.Eg-Umz5kPfewKrfm3u2hwPU6pMne_V1OcA5bZbivm8I"
              }

    datas = {
        "sql": "select * from goods_display_order_brother  where effective_cat_id = 7  order by sales_order_28_days DESC ",
        "basename": "azazie", "source": "azdbslave"}
    goods_list = []
    url = 'https://audit-az.gaoyaya.com/api/v2/query'
    res = requests.post(url, headers=header, json=datas)
    print(res.json()['data'])


def update_order_info():
    """
    更改order_info的language & country
    国家表 ：region
    语言表：language表
    :return:
    """
    country_list = {
        "us_en": [3859, 1],
        "us_es": [3859, 3],
        "fr": [4003, 4],
        "de": [4017, 2],
        "es": [4143, 3],
        "it": [4056, 7],
        "nl": [4099, 12],
        "se": [4202, 5]}
    az_db = Database(
        user='azazie',
        password='azazie',
        host='db-zt.opsfun.com',
        port=3306,
        database='azazie'

    )
    for k, v in country_list.items():
        print(k, v)
        sql = f"UPDATE order_info SET country = {v[0]}, language_id = {v[1]} WHERE order_sn ='ZZ4577727150';"
        az_db.alterData(sql)

        while True:
            value = input('next ??:')
            if value == 'y':
                break
            else:
                continue


def updateCouponEndTime(email, coupon_code, end_time):
    az_db = Database(
        user='azazie',
        password='azazie',
        host='az-test-db.gaoyaya.com',
        port=3306,
        database='azazie'

    )
    sql_select_coupon_id = f"select id from coupon_user_map where email = '{email}' and coupon_code = '{coupon_code}'"
    id = az_db.getFetchall(sql_select_coupon_id)[0]['id']
    sql_update_etime = f"update  coupon_user_map set coupon_end_time = '{end_time}' where id = '{id}'"
    az_db.updateDate(sql_update_etime)
    sql_select_coupon_end_time = f"select coupon_end_time  from coupon_user_map where id = '{id}'"
    coupon_end_time = az_db.getFetchall(sql_select_coupon_end_time)[0]['coupon_end_time']
    print('coupon_code:', coupon_code, 'id:', id)
    return coupon_end_time


def remaining_time_until_given_timestamp(timestamp, coupon_code):
    # 获取当前洛杉矶时间
    la_timezone = timezone(timedelta(hours=-7))  # 洛杉矶夏令时时区 UTC-7
    current_time_utc = datetime.now(timezone.utc)  # 当前UTC时间
    current_time_la = current_time_utc.astimezone(la_timezone)

    # 将时间戳转换为 datetime 对象（带有时区信息）
    given_time = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)

    # 计算剩余时间
    remaining_time = given_time - current_time_utc

    remaining_days = remaining_time.days
    remaining_hours, remainder_seconds = divmod(remaining_time.seconds, 3600)

    print(f"coupon code: {coupon_code} 失效时间剩余 {remaining_days} 天 {remaining_hours} 小时")

    return remaining_days, remaining_hours


def format_email():
    timestamp = int(time.time())
    date = time.strftime('%m%d%H%M%S', time.localtime(timestamp))
    email = f'test_shiyong{date}@gaoyaya.com'
    print(email)
    return email


if __name__ == '__main__':
    # 调用函数并传入时间戳和优惠券代码
    # given_timestamp = 1725415199  # 替换为你的时间戳
    # coupon_code = "YOUR_COUPON_CODE"  # 替换为你的优惠券代码
    # remaining_time_until_given_timestamp(given_timestamp, coupon_code)

    # format_email()

    token = loginAZ(is_pro=True)
    rec_id_list = getRecId(token)
    deleteCard(rec_id_list, token, True)

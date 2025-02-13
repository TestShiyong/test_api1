import requests
from common.handleDatabase import Database

from datetime import datetime, timezone, timedelta
import time
from common.handleDatabase import az_db

# BASE_ULR = 'https://api-t-7.azazie.com'


BASE_ULR = 'https://apix.azazie.com'


def loginAZ():
    url = BASE_ULR + '/1.0/user/login'

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
    url = BASE_ULR + '/1.0/cart'
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
        url = BASE_ULR + f'/1.0/cart/goods/{rec_id}'
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
    print('detail color :', li)


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


def format_email():
    timestamp = int(time.time())
    date = time.strftime('%m%d%H%M%S', time.localtime(timestamp))
    email = f'test_shiyong{date}@gaoyaya.com'
    print(email)
    return email


def legoLogin():
    url = 'https://api-t-1-lego.azazie.com/auth/login'
    datas = {"username": "admin", "password": "lb123456"}
    res = requests.post(url, json=datas)
    token = res.json()['data']['token']
    return token


def azOnlineDatabase(sql, token):
    """
    从AZ数据库获取数据处理。
    """
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Connection": "keep-alive",
        "Host": "audit-az.gaoyaya.com",
        "Origin": "https://audit-az.gaoyaya.com",
        "Referer": "https://audit-az.gaoyaya.com/",
        "authorization": token
    }
    datas = {
        # "sql": "select * from goods_display_order_brother where effective_cat_id = 7 order by sales_order_28_days DESC ",
        "sql": sql,
        "basename": "azazie",
        "source": "azdbslave"
    }
    url = 'https://audit-az.gaoyaya.com/api/v2/query'
    res = requests.post(url, headers=header, json=datas)
    # 处理返回的数据...
    return res.json()


def removeDuplicates(lst):
    """
    从列表中移除重复项。

    参数：
        lst: 要处理的列表。

    返回：
        移除重复项后的列表。
    """
    return list(set(lst))


def getProductColors(goods_id):
    """
    调用first-screen获取商品的颜色信息。

    参数：
        goods_id: 商品ID。

    返回：
        包含颜色数量和商品名称的元组。
    """
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-app": "pc",
        "x-token": "",
        "x-project": "azazie",
        "x-countryCode": "US",
        "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
    }
    url = f'https://apix-p6.azazie.com/1.0/product/first-screen?goods_id={goods_id}'
    try:
        res = requests.get(url, headers=header)
        colors = res.json()['data']['styleInfo']['color']
        goods_name = res.json()['data']['baseInfo']['goodsName'].replace("Flower Girl Dress", "").strip()
        color_count = len(colors)
        return color_count, goods_name
    except Exception as e:
        print(f'数据异常 id:{goods_id}')


def get_goods_list(url, page_range, data):
    """
    从列表页接口返回数据中获取商品列表，并移除重复项。

    参数：
        url: 列表页接口URL。
        page_range: 页码范围。
        data: POST请求的数据。

    返回：
        商品列表。
    """
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-app": "pc",
        "x-token": "",
        "x-project": "azazie",
        "x-countryCode": "US",
        "authorization": "Basic bGViYmF5OnBhc3N3MHJk",
        "cache-action": "flush"
    }
    goods_list = []
    count_goods_list = {}
    for number in range(1, page_range):
        url_with_page = url.replace("page=1", f"page={number}")
        res = requests.post(url_with_page, json=data, headers=header)
        dict1 = res.json()['data']['prodList']
        for item in dict1:
            goods_list.append(item['goodsId'])

    unique_goods_list = removeDuplicates(goods_list)
    for goods in goods_list:
        count_goods_number = goods_list.count(goods)
        count_goods_list[goods] = count_goods_number
    print(unique_goods_list)
    print('unique_goods_list数量:', len(unique_goods_list))
    print(goods_list)
    print('goods_list数量',len(goods_list))
    print(count_goods_list)
    # # print(f"Total number of goods: {len(unique_goods_list)}")
    # for item_id in unique_goods_list:
    #     count_color_number = getProductColors(item_id)
    #     print(
    #         f"Item ID: {item_id}, Count_goods: {goods_list.count(item_id)}, Count_color_number: {count_color_number[0]} - {count_color_number[1]}")





    """
        url2 ="https://p.azazie.com/pre/1.0/list/content-new?format=list&cat_name=atelier-gala-dresses&dress_type=dress&page=1&limit=60&in_stock=&sort_by=popularity&is_outlet=0&version=b&activityVerison=a&galleryVersion=A&sodGalleryVersion=B&topic=azazie&listColorVersion=A&multiColorVersion=b&show_final_sale=0"
    data = {"filters":{},"view_mode":["petite"],"originUrl":"/all/atelier-gala-dresses?sort_by=popularity&page=1"}
    url="https://www.azazie.com/prod/1.0/list/content-new?format=list&cat_name=atelier-gala-dresses&dress_type=dress&page=1&limit=60&in_stock=&sort_by=popularity&is_outlet=0&version=b&activityVerison=a&galleryVersion=A&sodGalleryVersion=B&topic=azazie&listColorVersion=A&multiColorVersion=b&show_final_sale=0"
    goods_list = get_goods_list(url, 8, data)
    print(goods_list)
    """


    return unique_goods_list

def getColorId(color_name, cat_id):
    from common.handleDatabase import az_db
    sql = f"	SELECT * FROM `style` where value  ='Barbie™ Pink' and `name` = 'color' and cat_id ={cat_id} "
    res = az_db.getFetchone(sql)
    style_id = res['style_id']
    print(f'color : ({color_name})，style_id : {style_id}')
    return style_id


def joinSku(cat_id, goods_id, color_id, size_id):
    if size_id:
        print(f'ZZc{cat_id}g{goods_id}y{color_id}s{size_id}')
    else:
        print(f'ZZc{cat_id}g{goods_id}c{cat_id}')


def getSkuDetails(sku):
    """
    传入sku后连接数据库查询  然后输出color 与 size的name
    :param sku:
    :return:
    """
    from common.handleDatabase import az_db
    g_index = sku.find('g')
    y_index = sku.find('y')
    s_index = sku.find('s')
    goods_id = sku[g_index + 1:y_index]
    color_id = sku[y_index + 1:s_index]
    size_id = sku[s_index + 1:]

    sql_get_size_name = f"SELECT `value` FROM `style` where style_id = {size_id} and `name` = 'Size'"
    sql_get_color_name = f"SELECT `value` FROM `style` where style_id = {color_id} and `name` ='Color';"
    size_name = az_db.getFetchone(sql_get_size_name)['value']
    color_name = az_db.getFetchone(sql_get_color_name)['value']
    print(
        f'goods_id({goods_id}),\ncolor_id({color_id}),\nsize_id({size_id}),\ncolor_name({color_name}),\nsize_name({size_name})')


if __name__ == '__main__':
    # format_email()
    #
    # token = loginAZ()
    # rec_id_list = getRecId(token)
    # deleteCard(rec_id_list, token, True)
    #
    # # detail_page_colors(1066990)
    #
    # # getColorId('Barbie™ Pink',7)
    # sku = 'ZZc7g1004430y196s7493'
    # getSkuDetails(sku)
    joinSku(7, 1051103, 7754, 7491)
    # sql =''
    # az_db.getFetchall()


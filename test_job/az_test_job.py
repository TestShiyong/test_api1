import requests
from common.handle_database import Database
import main



def group_list(l1):
    l2 = []
    for goods in l1:
        if goods not in l2:
            l2.append(goods)
    return l2


import requests


def group_goods(url, page_numbers):
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
    data = {"filters": {}, "view_mode": ["petite"], "originUrl": url}

    goods_list = []
    for number in range(*page_numbers):
        url_with_page = url.replace("page=1", f"page={number}")
        res = requests.post(url_with_page, json=data, headers=header)
        dict1 = res.json()['data']['prodList']
        for item in dict1:
            goods_list.append(item['goodsId'])
    no_duplicates = group_list(goods_list)
    print(f"Total number of goods: {len(goods_list)}")
    print(goods_list)
    for item_id in no_duplicates:
        print(f"Item ID: {item_id}, Count: {goods_list.count(item_id)}")
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
              "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
              }

    datas = {
        "sql": "select * from goods_display_order_brother  where effective_cat_id = 7  order by sales_order_28_days DESC ",
        "basename": "azazie", "source": "azdbslave"}
    goods_list = []
    url = 'https://audit-az.gaoyaya.com/api/v2/query'
    res = requests.post(url, headers=header, json=datas)


"""

"""


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
        az_db.alter_data(sql)

        while True:
            value = input('next ??:')
            if value == 'y':
                break
            else:
                continue



pro_url = 'https://www.azazie.com/prod/1.0/list/content?format=list&cat_name=flower-girl-dresses&dress_type=dress&page=1&limit=60&in_stock=&sort_by=popularity&is_outlet=0&version=b&activityVerison=a&galleryVersion=B&sodGalleryVersion=B&topic=azazie&listColorVersion=A'
pre_url = 'https://p6.azazie.com/pre/1.0/list/content?format=list&cat_name=flower-girl-dresses&dress_type=dress&page=1&limit=60&in_stock=&sort_by=popularity&is_outlet=0&version=b&activityVerison=a&galleryVersion=B&sodGalleryVersion=B&topic=azazie&listColorVersion=A'
group_goods(pro_url, (1, 7))
group_goods(pre_url, (1, 5))


import requests
from common.handle_database import Database
import main


def group_goods():
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
    data = {"filters": {}, "view_mode": ["petite"], "originUrl": "/all/flower-girl-dresses?sort_by=popularity&page=1"}

    goods_list = []
    for i in range(1, 7):
        url = f'https://p6.azazie.com/pre/1.0/list/content?format=list&cat_name=flower-girl-dresses&dress_type=dress&page={i}&limit=60&in_stock=&sort_by=popularity&is_outlet=0&version=b&activityVerison=a&galleryVersion=A&sodGalleryVersion=B&topic=azazie&listColorVersion=A'
        res = requests.post(url, json=data, headers=header)
        dict1 = res.json()['data']['prodList']
        for i in dict1:
            goods_list.append(i['goodsId'])
    print(len(goods_list), print(goods_list))
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


# group_goods()
update_order_info()

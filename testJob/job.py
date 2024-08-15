import requests

from common.handleDatabase import Database


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
    获取商品的颜色信息。

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
    for number in range(*page_range):
        url_with_page = url.replace("page=1", f"page={number}")
        res = requests.post(url_with_page, json=data, headers=header)
        dict1 = res.json()['data']['prodList']
        for item in dict1:
            goods_list.append(item['goodsId'])
    unique_goods_list = removeDuplicates(goods_list)
    print(f"Total number of goods: {len(unique_goods_list)}")
    for item_id in unique_goods_list:
        count_color_number = getProductColors(item_id)
        print(
            f"Item ID: {item_id}, Count_goods: {goods_list.count(item_id)}, Count_color_number: {count_color_number[0]} - {count_color_number[1]}")
    return unique_goods_list


def get_goods_data_from_az_database():
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
        "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
    }
    datas = {
        "sql": "select * from goods_display_order_brother where effective_cat_id = 7 order by sales_order_28_days DESC ",
        "basename": "azazie",
        "source": "azdbslave"
    }
    url = 'https://audit-az.gaoyaya.com/api/v2/query'
    res = requests.post(url, headers=header, json=datas)
    # 处理返回的数据...


def update_order_info():
    """
    更新订单信息。
    """
    country_list = {
        "us_en": [3859, 1],
        "us_es": [3859, 3],
        "fr": [4003, 4],
        "de": [4017, 2],
        "es": [4143, 3],
        "it": [4056, 7],
        "nl": [4099, 12],
        "se": [4202, 5]
    }
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


flower_url = 'https://p6.azazie.com/pre/1.0/list/content?format=list&cat_name=flower-girl-dresses&dress_type=dress&page=1&limit=60&in_stock=&sort_by=popularity&is_outlet=0&version=b&activityVerison=b&galleryVersion=A&sodGalleryVersion=B&topic=azazie&listColorVersion=A'
flower_datas = {"filters": {}, "view_mode": ["petite"],
                "originUrl": "/all/flower-girl-dresses?sort_by=popularity&page=1"}
get_goods_list(flower_url, (1, 6), flower_datas)

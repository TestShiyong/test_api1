import requests

header = {"Content-Type": "application/json;charset=UTF-8",
          "Accept": "application/json, text/plain, */*",
          "Connection": "keep-alive",
          "Host": "audit-az.gaoyaya.com",
          "Origin": "https://audit-az.gaoyaya.com",
          "Referer": "https://audit-az.gaoyaya.com/",
          "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDUzMzY4ODksIm5hbWUiOiJzaGl5b25nIiwicm9sZSI6Imd1ZXN0In0.giUCEjl6Md0OietzbC8bFdO20Pbxnei5p29Fcy1kcns",
          "Sec-Fetch-Site": "same-origin",
          "Sec-Ch-Ua-Platform": "Windows",
          "Sec-Fetch-Mode": "cors",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.9",

          }


def group_goods():
    datas = {"sql":"select * from goods_display_order_brother  where effective_cat_id = 7  order by sales_order_28_days DESC ","basename":"azazie","source":"azdbslave"}
    goods_list = []
    url = 'https://audit-az.gaoyaya.com/api/v2/query'
    res = requests.post(url, headers=header, json=datas).json()
    for i in res:
        goods_list.append(i['goods_id'])
    li = [1052929,1052888,1056567,1003925]
    for i in li:
        print(goods_list.index(i))

group_goods()

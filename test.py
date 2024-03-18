import requests


def list_content():
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "x-app": "pc",
               "x-token": "",
               "x-project": "azazie",
               "x-countryCode": "US",
               "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
               }
    url = 'https://www.azazie.com/prod/1.0/list/content?cat_name=ready-to-ship-bridesmaids&dress_type=clearance&page=1&limit=60&in_stock=yes&sort_by=popularity&current_in_stock=yes&is_outlet=0&version=b&activityVerison=b&galleryVersion=A&sodGalleryVersion=B&listColorVersion=A'

    res = requests.post(url, headers=headers)
    goods_lsit = res.json()['data']['goodsIdList']
    print(goods_lsit)
    return goods_lsit


def rts_stock_filter(goods):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "x-app": "pc",
               "x-token": "",
               "x-project": "azazie",
               "x-countryCode": "US",
               "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
               }

    url = f'https://apix.azazie.com/1.0/stock/{goods}?discount=3&dress_type=clearance'
    res = requests.get(url, headers=headers)

    stockNumberMap1 = res.json()
    if stockNumberMap1['data']['hasStock']:
        stockNumberMap = res.json()['data']['stockNumberMap']

        list1 = []
        for k, y in stockNumberMap.items():
            list1.append(k.split('*'))
        print(goods)
    else:
        return False
    return list1


def return_warehouse(goods_id, color, size):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "x-app": "pc",
               "x-token": "",
               "x-project": "azazie",
               "x-countryCode": "US",
               "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
               }

    url = f'https://p5.azazie.com/pre/1.0/product/item-info?goods_id={goods_id}' \
          f'&dress_type=clearance&color={color}&size={size}&from=product'

    res = requests.get(url, headers=headers)
    warehouse = res.json()['data']['baseInfo']['warehouse']
    if warehouse:
        print('有值', goods_id, color, size)


goods_list = list_content()[40:]
def return_goods(goods_list):
    for i in goods_list:
        goods_items = rts_stock_filter(i)
        if goods_items:
            for j in goods_items:
                return_warehouse(i, j[0], j[1])
        else:
            continue

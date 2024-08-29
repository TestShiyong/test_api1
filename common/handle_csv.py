from common.handleData import GlobalData
import myPath
import csv
import random
from common.handle_request import sendRequest
from common.handleConfig import ConfigReader
from common.handleData import replaceAllData
from jsonpath import jsonpath
import re

BASE_URL = ConfigReader.getStr('Url', 'PROD_URL')


def getColorAndSize(goods_id):
    """
    调用首屏接口 获取color size id
    :param goods_id:
    :return: color_id, size_id
    """
    url = BASE_URL + f'1.0/product/first-screen?goods_id={goods_id}'
    res = sendRequest('get', url, output=False)
    color = random.choice([key for key in res.json()['data']['styleInfo']['color']])
    color_id = res.json()['data']['styleInfo']['color'][color]['styleId']

    size = random.choice([size for size in res.json()['data']['styleInfo']['size']])
    size_id = size['styleId']

    return color_id, size_id


def waiteDataCav(file_path, goods_data):
    """
    #goods测试数据到csv文件
    :param file_path:
    :param goods_data:
    :return:
    """
    with open(file_path, mode='w', encoding='utf-8', newline="") as f:
        headers = ["goods_id", "goods_name", "cat_id", "shop_price", "shop_price",
                   "no_deal_price", "dress_type", "price_symbol", "goods_sn", "market_price"]
        write = csv.DictWriter(f, headers)
        write.writeheader()
        write.writerows(goods_data)


def read_csv(file_path):
    li = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            li.append(dict(row))
    return li


def random_csv_data(file):
    goods_list = read_csv(file)
    goods_data = random.choice(goods_list)
    return goods_data


def handle_cart_data(file, case):
    goods_data = random_csv_data(file)
    goods_id = goods_data['goods_id']
    color_id, size_id = getColorAndSize(goods_id)
    setattr(GlobalData, "goods_id", goods_id)
    setattr(GlobalData, "color_id", str(color_id))
    setattr(GlobalData, "size_id", str(size_id))

    case = replaceAllData(case)
    return case


he = {"Content-Type": "application/json", "x-app": "pc", "x-token": "${token}", "x-project": "azazie",
      "x-countryCode": "US"}


def new_replace(case):
    for key, value in case.items():
        if value is not None and isinstance(value, str):
            case[key] = replace_data(value)
        elif value is not None and isinstance(value, dict):
            for k, v in value.items():
                if v is not None and isinstance(v, str):
                    case[k] = replace_data(value)
    return case


def replace_data(replace_str):
    res = re.findall('#(.*?)#', replace_str)
    if res:
        for mark_data in res:
            try:
                value = getattr(GlobalData, mark_data)
            except:
                try:
                    value = ConfigReader.getStr('', str(mark_data))
                except:
                    continue
            replace_str = replace_str.replace("#{}#".format(mark_data), value)
    return replace_str


if __name__ == '__main__':
    path = r"C:\Users\15572\Desktop\test\test_api\prime_data\all_bridesmaid_dresses.csv"

    goods_list = read_csv(path)
    goods_info = random.choice(goods_list)
    print(goods_info)
    pass

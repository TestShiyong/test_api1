from common.handle_data import GlobalVar
import mypath
import csv
import random
from common.handle_request import send_request
from common.handle_conf_file import cf, base_url
from common.handle_data import replace_all_data
from jsonpath import jsonpath
import re

base_url = base_url


def color_size(goods_id):
    """
    调用首屏接口 获取color size id
    :param goods_id:
    :return: color_id, size_id
    """
    url = base_url + f'1.0/product/first-screen?goods_id={goods_id}'
    res = send_request('get', url, out_put=False)
    color = random.choice([key for key in res.json()['data']['styleInfo']['color']])
    color_id = res.json()['data']['styleInfo']['color'][color]['styleId']

    size = random.choice([size for size in res.json()['data']['styleInfo']['size']])
    size_id = size['styleId']

    return color_id, size_id


def waite_data_cav(file_path, goods_data):
    with open(file_path, mode='w', encoding='utf-8', newline="") as f:
        headers = ["goods_id", "goods_name", "cat_id", "shop_price", "shop_price",
                   "no_deal_price", "dress_type", "price_symbol", "goods_sn", "market_price"]
        write = csv.DictWriter(f, headers)
        write.writeheader()
        write.writerows(goods_data)

        # except:
        #     header = ["goods_id", "cat_id", "goods_name", "color_style_id", "size_style_id", "shop_price",
        #               "no_deal_price"]
        #     write = csv.DictWriter(f, header)
        #     write.writeheader()
        #     write.writerows(goods_data)


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
    color_id, size_id = color_size(goods_id)
    setattr(GlobalVar, "goods_id", goods_id)
    setattr(GlobalVar, "color_id", str(color_id))
    setattr(GlobalVar, "size_id", str(size_id))

    case = replace_all_data(case)
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
                value = getattr(GlobalVar, mark_data)
            except:
                try:
                    value = cf.get_str('', str(mark_data))
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

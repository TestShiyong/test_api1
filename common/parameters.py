from common.handleCsv import read_csv

import random
import re
from jsonpath import jsonpath


def __parameter(file):
    return read_csv(file)


def random_data(file):
    goods = __parameter(file)
    return random.choice(goods)


def replace_data(case, csv_data, re_data):
    li = re.findall("#(.*?)#", re_data)
    if li:
        for i in li:
            value = jsonpath(csv_data, i)


def csv_data(case, file):
    goods_data = random_data(file)
    print(goods_data)
    for k, v in case.items():
        if v is not None and isinstance(v, str):
            li = re.findall("#(.*?)#", v)
            if li:
                for i in li:
                    value = jsonpath(goods_data, i)[0]
                    case[k] = value
    return case


aa = {
    "goods_id": "#goods_id#",
    "dress_type": "dress",
    "from_showroom": "",
    "from_whatAreU": "",
    "recommend_flag": "",
    "from_details_entry": "",
    "from_instagram": "",
    "styles": {
        "freeStyle": False,
        "size_type": "_inch",
        "select": {
            "color": '#color_id#',
            "size": "$size_id#"
        }
    },
    "goods_number": 1
}

if __name__ == '__main__':
    # print(random_data(r'C:\Users\15572\Desktop\test\test_api\prime_data\all_bridesmaid_dresses.csv'))
    print(csv_data(aa, r'C:\Users\15572\Desktop\test\test_api\prime_data\all_bridesmaid_dresses.csv'))

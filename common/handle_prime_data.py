parameters.pyfrom common.dress_type import all_dress_type
from common.handle_request import send_request
from common.handle_conf_file import cf
from common.handle_csv import waite_data_cav
import mypath
import os
import queue
from threading import Thread


# def preset_data():
#     base_url = cf.get_str('Url', 'TEST_URL')
#     # test
#     base_url = cf.get_str('Url', 'PROD_URL')
#     # 遍历goods type
#     for cat_name in all_dress_type:
#         if 'sample' in cat_name[0]:
#             url = f'/list/content?cat_name={cat_name[0]}&dress_type=sample&page=1&limit=30&page=1'
#         elif 'ready-to-ship' in cat_name[0]:
#             url = f'/list/content?cat_name={cat_name[0]}&dress_type=clearance&page=1&limit=30&page=1'
#         elif 'outlet' in cat_name[0]:
#             url = f'/list/content?cat_name={cat_name[0]}&dress_type=outlet&page=1&limit=30&page=1'
#         else:
#             url = f'/list/content?cat_name={cat_name[0]}&dress_type=dress&page=1&limit=30&page=1'
#         res = send_request('post', url=base_url + url,out_put=False)
#         path = os.path.join(mypath.prime_data_dir, cat_name[1])
#         product_info_list = []
#         for i in res.json()["data"]["prodList"]:
#             goods_id = str(i["goodsId"])
#             goods_name = i["goodsName"]
#             cat_id = str(i["catId"])
#             shop_price = str(i["shopPrice"])
#             no_deal_price = str(i['noDealPrice'])
#             dress_type = i["dressType"]
#             price_symbol = i['priceSymbol']
#             goods_sn = i['goodsSn']
#             market_price = i['marketPrice']
#
#             product_info_list.append(
#                 {"goods_id": goods_id, "goods_name": goods_name, "cat_id": cat_id, "shop_price": shop_price,
#                  "no_deal_price": no_deal_price, "dress_type": dress_type, "price_symbol": price_symbol,
#                  "goods_sn": goods_sn, "market_price": market_price})
#         waite_data_cav(path,product_info_list)
#
#


def preset_data_work(que):
    base_url = cf.get_str('Url', 'TEST_URL')
    # test
    base_url = cf.get_str('Url', 'PROD_URL')
    while que.qsize() is not None:
        cat_name = que.get(timeout=0.1)

        if 'sample' in cat_name[0]:
            url = f'/list/content?cat_name={cat_name[0]}&dress_type=sample&page=1&limit=30&page=1'
        elif 'ready-to-ship' in cat_name[0]:
            url = f'/list/content?cat_name={cat_name[0]}&dress_type=clearance&page=1&limit=30&page=1'
        elif 'outlet' in cat_name[0]:
            url = f'/list/content?cat_name={cat_name[0]}&dress_type=outlet&page=1&limit=30&page=1'
        else:
            url = f'/list/content?cat_name={cat_name[0]}&dress_type=dress&page=1&limit=30&page=1'
        res = send_request('post', url=base_url + url, out_put=False)
        path = os.path.join(mypath.prime_data_dir, cat_name[1])
        product_info_list = []
        for i in res.json()["data"]["prodList"]:
            goods_id = str(i["goodsId"])
            goods_name = i["goodsName"]
            cat_id = str(i["catId"])
            shop_price = str(i["shopPrice"])
            no_deal_price = str(i['noDealPrice'])
            dress_type = i["dressType"]
            price_symbol = i['priceSymbol']
            goods_sn = i['goodsSn']
            market_price = i['marketPrice']

            product_info_list.append(
                {"goods_id": goods_id, "goods_name": goods_name, "cat_id": cat_id, "shop_price": shop_price,
                 "no_deal_price": no_deal_price, "dress_type": dress_type, "price_symbol": price_symbol,
                 "goods_sn": goods_sn, "market_price": market_price})
        waite_data_cav(path, product_info_list)


if __name__ == '__main__':
    que = queue.Queue()
    # 遍历goods type
    for cat_names in all_dress_type:
        que.put(cat_names)

    thread_obj_list = []
    for i in range(5):
        thread_obj = Thread(target=preset_data_work, args=(que,))
        thread_obj_list.append(thread_obj)

    for obj in thread_obj_list:
        obj.start()

    for item in thread_obj_list:
        item.join()

    # preset_data()

import time
from threading import Thread
from common.handleRequest import sendRequest
from common.handleConfig import cf
from common.handleLog import log
from common.handleCsv import waite_data_cav
import random
import myPath
import os


class GoodsFilter:

    def __init__(self, even, cat_name, platform, dress_type, page, country, limit=48):
        self.even = even
        self.cat_name = cat_name
        self.platform = platform
        self.dress_type = dress_type
        self.page = page
        self.limit = limit
        self.country = country
        self.headers = {"Content-Type": "application/json", "x-app": self.platform, "x-token": "",
                        "x-project": "azazie", "x-countryCode": self.country}

    def list_product(self):
        """
        [{'goodsId': item['goodsId'], 'catId': item['catId'], 'goodsName': item['goodsName']}] 加入队列

        :return: 返回列表页 整页48个商品数据 [{'goodsId': item['goodsId'], 'catId': item['catId'], 'goodsName': item['goodsName']}]
        """
        url = self.even + f'/list/content?cat_name={self.cat_name}' \
                          f'&dress_type={self.dress_type}' \
                          f'&page={self.page}&' \
                          f'in_stock=yes&current_in_stock=yes&'
        goods_pro_list = sendRequest('post', url, headers=self.headers, output=False).json()['data']['prodList']

        goods_list = [{'goods_id': item['goodsId'], 'cat_id': item['catId'], 'goods_name': item['goodsName']}
                      for item in goods_pro_list]
        return goods_list

    def __no_batch_goods_filter_stock(self, goods_id):
        url = self.even + '/stock/{}'.format(goods_id)
        res = sendRequest('get', url, headers=self.headers, output=False)
        if res.json()['data']['hasStock']:
            list_map = [{'map': key, "value": value} for key, value in res.json()['data']['stockNumberMap'].items()]

            max_stock_color = sorted(list_map, key=lambda i: i['value'], reverse=True)[0]
            print({"color": max_stock_color['map'].split('*')[0], "size": max_stock_color['map'].split('*')[1],
                   "num": max_stock_color['value']})
            return {"color": max_stock_color['map'].split('*')[0], "size": max_stock_color['map'].split('*')[1],
                    "num": max_stock_color['value']}
        else:
            return None

    def get_no_batch_detail_data(self, goods_id):
        color_size = self.__no_batch_goods_filter_stock(goods_id)
        if color_size:
            url = self.even + '/product/first-screen?goods_id={}'.format(goods_id)
            res = sendRequest('get', url, headers=self.headers, output=False)
            try:
                color_style_id = res.json()['data']['styleInfo']['color'][color_size['color']]['styleId']
            except:
                color_style_id = res.json()['data']['styleInfo']['color'][color_size['color_name']]['styleId']

            style_info = size_style_id = res.json()['data']['styleInfo']['size']
            for i in style_info:
                if i['key'] == color_size['size']:
                    size_style_id = i['styleId']
            shop_price = res.json()['data']['baseInfo']['shopPrice']
            no_deal_price = res.json()['data']['baseInfo']['noDealPrice']
            return {"color_style_id": color_style_id, "size_style_id": size_style_id, "shop_price": shop_price,
                    "no_deal_price": no_deal_price}
        else:
            return None

    def get_no_batch_data(self):
        list_all_no_batch_data = []
        good_item = self.list_product()
        for items in good_item:
            goods_detail = self.get_no_batch_detail_data(items["goods_id"])
            if goods_detail:
                list_all_no_batch_data.append(
                    {"goods_id": items["goods_id"], "cat_id": items["cat_id"], "goods_name": items["goods_name"],
                     "color_style_id": goods_detail["color_style_id"], "size_style_id": goods_detail['size_style_id'],
                     "shop_price": goods_detail['shop_price'], "no_deal_price": goods_detail['no_deal_price']})

        print(list_all_no_batch_data)
        return list_all_no_batch_data

    def batch_random_color_size(self, goods_id):
        """
        前置：list_product 方法吧
        :param list_goods_data:
        :param g_name:
        :return:
        """
        url = self.even + f'1.0/product/first-screen?goods_id={goods_id}'
        res = sendRequest('get', url, headers=self.headers, output=False)
        color = random.choice([key for key in res.json()['data']['styleInfo']['color']])
        color_id = res.json()['data']['styleInfo']['color'][color]['styleId']

        size = random.choice([size for size in res.json()['data']['styleInfo']['size']])
        size_id = size['styleId']

        shop_price = res.json()['data']['baseInfo']['shopPrice']
        no_deal_price = res.json()['data']['baseInfo']['noDealPrice']
        log.info('goods 随机获取color:(color_name:{},color_id:{}),size:(size_name:{},size_id:{})'.format(color,
                                                                                                     color_id,
                                                                                                     size['name'],
                                                                                                     size_id))

        return {"color_style_id": color_id, "size_style_id": size_id, "shop_price": shop_price,
                "no_deal_price": no_deal_price}

    def get_batch_data(self):
        all_batch_data = []
        prod_list_goods = self.list_product()
        for item in prod_list_goods:
            color_size_id = self.batch_random_color_size(item['goods_id'])
            if color_size_id:
                all_batch_data.append(
                    {"goods_id": item['goods_id'], "cat_id": item['cat_id'], "goods_name": item['goods_name'],
                     "color_style_id": color_size_id['color_style_id'], "size_style_id": color_size_id['size_style_id'],
                     "shop_price": color_size_id['shop_price'], "no_deal_price": color_size_id['no_deal_price']})
            else:
                continue
        print(all_batch_data)
        return all_batch_data

    def waite_bath(self):
        goods_info = self.get_batch_data()
        waite_data_cav(os.path.join(myPath.prime_data_dir, 'wedding-dresses.csv'), goods_info)

    def waite_no_bath(self):
        goods_info = self.get_no_batch_data()
        waite_data_cav(os.path.join(myPath.prime_data_dir, self.dress_type), goods_info)


if __name__ == '__main__':
    batch_goods = GoodsFilter(even=cf.get_str('Url', 'TEST_URL'),
                              cat_name='wedding-dresses',
                              platform='pc',
                              dress_type='dress',
                              page='1',
                              country='us')

    no_batch_goods = GoodsFilter(even=cf.get_str('Url', 'TEST_URL'),
                                 cat_name='dresses',
                                 platform='pc',
                                 dress_type='dress',
                                 page='1',
                                 country='us')

    # batch_goods.waite_bath()
    no_batch_goods.waite_no_bath()

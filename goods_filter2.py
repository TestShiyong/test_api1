import time
from threading import Thread
from common.handle_request import send_request
from common.handle_red_conf_file import cf
from common.handle_log import log
import random


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
        goods_pro_list = send_request('post', url, country=self.country, output=False).json()['data']['prodList']

        goods_list = [{'goods_id': item['goodsId'], 'cat_id': item['catId'], 'goods_name': item['goodsName']}
                      for item in goods_pro_list]
        return goods_list

    def __no_batch_get_color_size(self, goods_id):
        """
        前置：list_product 方法吧
        :param list_goods_data:
        :param g_name:
        :return:
        """
        url = self.even + f'/product/first-screen?goods_id={goods_id}'
        res = send_request('get', url, country=self.country, output=False)
        color = random.choice([key for key in res.json()['data']['styleInfo']['color']])
        color_id = res.json()['data']['styleInfo']['color'][color]['styleId']

        size = random.choice([size for size in res.json()['data']['styleInfo']['size']])
        size_id = size['styleId']
        log.info('goods 随机获取color:(color_name:{},color_id:{}),size:(size_name:{},size_id:{})'.format(color,
                                                                                                     color_id,
                                                                                                     size['name'],
                                                                                                     size_id))

        return {"colorId": color_id, "sizeId": size_id}

    def all_no_batch_data(self):
        list_all_no_batch_data = []
        good_item = self.list_product()
        for items in good_item:
            color_size = self.__no_batch_get_color_size(items["goodsId"])
            list_all_no_batch_data.append(
                {"goodsId": items["goodsId"], "catId": items["catId"], "goodsName": items["goodsName"],
                 "colorId": color_size["colorId"], "sizeId": color_size['sizeId']})
        print(list_all_no_batch_data)

    def __batch_goods_filter_stock(self, goods_id):
        url = self.even + '/stock/{}'.format(goods_id)
        res = send_request('get', url, self.country)
        if res.json()['data']['hasStock']:
            list_map = [{'map': key, "value": value} for key, value in res.json()['data']['stockNumberMap'].items()]

            max_stock_color = sorted(list_map, key=lambda i: i['value'], reverse=True)[0]
            return {"color_name": max_stock_color['map'].split('*')[0], "size_name": max_stock_color['map'].split('*')[1],
                    "num": max_stock_color['value']}
        else:
            return None

    def __get_batch_color_size_id(self, goods_id):
        color_size_name = self.__batch_goods_filter_stock(goods_id)
        if color_size_name:
            url = self.even + '/product/first-screen?goods_id={}'.format(goods_id)
            res = send_request('get', url, self.country)
            color_style_id = res.json()['data']['styleInfo']['color'][color_size_name['color_name']]['styleId']

            style_info = size_style_id = res.json()['data']['styleInfo']['size']
            for i in style_info:
                if i['key'] == color_size_name['size_name']:
                    size_style_id = i['styleId']
            shop_price = res.json()['data']['baseInfo']['shopPrice']
            no_deal_price = res.json()['data']['baseInfo']['noDealPrice']
            return {"color_style_id": color_style_id, "size_style_id": size_style_id, "shop_price": shop_price,
                    "no_deal_price": no_deal_price}
        else:
            return None

    def all_batch_data(self):
        all_batch_data = []
        prod_list_goods = self.list_product()
        for item in prod_list_goods:
            color_size_id = self.__get_batch_color_size_id(item['goods_id'])
            if color_size_id:
                all_batch_data.append(
                    {"goods_id": item['goods_id'], "cat_id": item['cat_id'], "goods_name": item['goods_name'],
                     "color_style_id": color_size_id['color_style_id'], "size_style_id": color_size_id['size_style_id'],
                     "shop_price": color_size_id['shop_price'], "no_deal_price": color_size_id['no_deal_price']})
            else:
                continue
        print(all_batch_data)
        return all_batch_data


if __name__ == '__main__':
    # no_batch_goods = GoodsFilter(even=cf.get_str('Url', 'TEST_URL'),
    #                              cat_name='wedding-dresses',
    #                              platform='pc',
    #                              dress_type='dress',
    #                              page='1',
    #                              country='us')

    batch_goods = GoodsFilter(even=cf.get_str('Url', 'TEST_URL'),
                              cat_name='dresses',
                              platform='pc',
                              dress_type='dress',
                              page='1',
                              country='us')

    batch_goods.all_batch_data()
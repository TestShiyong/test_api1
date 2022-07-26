import time
from threading import Thread
from common.handle_request import send_request
from common.handle_red_conf_file import cf
from common.handle_log import log
import queue
import gevent
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
        self.que = queue.Queue()

    def list_product(self):
        goods_list = []
        """
        [{'goodsId': item['goodsId'], 'catId': item['catId'], 'goodsName': item['goodsName']}] 加入队列

        :return: 返回列表页 整页48个商品数据 [{'goodsId': item['goodsId'], 'catId': item['catId'], 'goodsName': item['goodsName']}]
        """
        url = self.even + f'/list/content?cat_name={self.cat_name}' \
                          f'&dress_type={self.dress_type}' \
                          f'&page={self.page}&' \
                          f'in_stock=yes&current_in_stock=yes&'
        goods_pro_list = send_request('post', url, country=self.country, output=False).json()['data']['prodList']

        for item in goods_pro_list:
            goods_list.append({'goods_id': item['goodsId'], 'cat_id': item['catId'], 'goods_name': item['goodsName']})
            self.que.put({'goods_id': item['goodsId'], 'cat_id': item['catId'], 'goods_name': item['goodsName']})
        return goods_list

    def __batch_goods_filter_stock(self, goods_id):
        url = self.even + '/stock/{}'.format(goods_id)
        res = send_request('get', url, self.country,output=False)
        if res.json()['data']['hasStock']:
            list_map = [{'map': key, "value": value} for key, value in res.json()['data']['stockNumberMap'].items()]

            max_stock_color = sorted(list_map, key=lambda i: i['value'], reverse=True)[0]
            return {"color_name": max_stock_color['map'].split('*')[0],
                    "size_name": max_stock_color['map'].split('*')[1],
                    "num": max_stock_color['value']}
        else:
            print('商品无库存({})'.format(goods_id))
            return None

    def get_batch_color_size_id(self, all_batch_data,t_name):
        while not self.que.empty():
            print(self.que.qsize())
            goods_dict = self.que.get(timeout=0.1)
            print('({})开始运行，goods_id:({})'.format(t_name, goods_dict['goods_id']))
            color_size_name = self.__batch_goods_filter_stock(goods_dict['goods_id'])
            if color_size_name:
                url = self.even + '/product/first-screen?goods_id={}'.format(goods_dict['goods_id'])
                res = send_request('get', url, self.country,output=False)
                color_style_id = res.json()['data']['styleInfo']['color'][color_size_name['color_name']]['styleId']

                style_info = size_style_id = res.json()['data']['styleInfo']['size']
                for i in style_info:
                    if i['key'] == color_size_name['size_name']:
                        size_style_id = i['styleId']
                shop_price = res.json()['data']['baseInfo']['shopPrice']
                no_deal_price = res.json()['data']['baseInfo']['noDealPrice']

                all_batch_data.append(
                    {"goods_id": goods_dict['goods_id'], "cat_id": goods_dict['cat_id'],
                     "goods_name": goods_dict['goods_name'],
                     "color_style_id": color_style_id, "size_style_id": size_style_id, "shop_price": shop_price,
                     "no_deal_price": no_deal_price})
            else:
                continue

    def all_batch_goods_data(self):
        list_goods_data = []
        st = time.time()
        self.list_product()
        th_obj = []
        for i in range(5):
            t_name = '(gevent ({}))'.format(i)
            th_obj.append(Thread(target=self.get_batch_color_size_id, args=(list_goods_data, t_name)))
            print('创线程 ({})成功'.format(i))

        for i in th_obj:
            i.start()
        for i in th_obj:
            i.join()
        print(list_goods_data)
        et = time.time()
        print(st - et)


if __name__ == '__main__':
    batch_goods = GoodsFilter(even=cf.get_str('Url', 'TEST_URL'),
                              cat_name='dresses',
                              platform='pc',
                              dress_type='dress',
                              page='1',
                              country='us')

    batch_goods.all_batch_goods_data()
    # batch_goods.list_product()

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

    def no_batch_get_color_size(self, list_goods_data, g_name):
        """
        前置：list_product 方法把获取到的数据 全部添加如队列
        如果队列不为空  取出队列goods 随机获取color  size id 生成字典数据 加入传入的list_goods_data列表中


        :param list_goods_data:
        :param g_name:
        :return:
        """
        while not self.que.empty():
            goods_dict = self.que.get(timeout=0.01)
            print('({})开始运行，goods_id:({})'.format(g_name, goods_dict['goods_id']))
            url = self.even + f'/product/first-screen?goods_id={goods_dict["goods_id"]}'

            res = send_request('get', url, country=self.country, output=False)

            color = random.choice([key for key in res.json()['data']['styleInfo']['color']])
            colorId = res.json()['data']['styleInfo']['color'][color]['styleId']

            size = random.choice([size for size in res.json()['data']['styleInfo']['size']])
            sizeId = size['styleId']

            log.info('goods 随机获取color:(color_name:{},color_id:{}),'
                     'size:(size_name:{},size_id:{})'.format(color, colorId, size['name'], sizeId))

            list_goods_data.append(
                {"goodsId": goods_dict["goods_id"], "catId": goods_dict["cat_id"], "goodsName": goods_dict["goods_name"],
                 "colorId": colorId, "sizeId": sizeId})

    def no_batch_goods_data(self):
        st = time.time()
        self.list_product()

        list_goods_data = []
        th_obj = []
        for i in range(10):
            t_name = '(gevent ({}))'.format(i)
            th_obj.append(Thread(target=self.no_batch_get_color_size, args=(list_goods_data, t_name)))
            print('创线程 ({})成功'.format(i))

        for i in th_obj:
            i.start()
        for i in th_obj:
            i.join()
        print(list_goods_data)
        et = time.time()
        print(st - et)



if __name__ == '__main__':
    no_batch_goods = GoodsFilter(even=cf.get_str('Url', 'TEST_URL'),
                                 cat_name='wedding-dresses',
                                 platform='pc',
                                 dress_type='dress',
                                 page='1',
                                 country='us')

    # batch_goods = GoodsFilter(even=cf.get_str('Url', 'TEST_URL'),
    #                           cat_name='dresses',
    #                           platform='pc',
    #                           dress_type='dress',
    #                           page='1',
    #                           country='us')
    # batch_goods.all_batch_goods_data()
    # data = batch_goods.list_product()
    # print(data)
    no_batch_goods.no_batch_goods_data()

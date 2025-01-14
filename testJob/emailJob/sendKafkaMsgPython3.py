# @cursor start
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
推送 首页 类别页 详情页 崩失脚本 推送后立即发送邮件
"""
from confluent_kafka import Producer
import json

email = 'test_shiyong1123154538@gaoyaya.com'
# us-es
# email = 'test_shiyong1123140637@gaoyaya.com'


home_data = {"airship_id": "979a2cef-6155-48fa-ae46-12416c512352", "client_id": "C587152A-47CC-4451-B797-0FA39252AD94",
             "country_code": "US", "email": email, "from_page": "home", "interval": "1d"}

# bounce_data = {
#     "client_id": "C587152A-47CC-4451-B797-0FA39252AD94",
#     "airship_id": "979a2cef-6155-48fa-ae46-12416c512352",
#     "country_code": "CA",
#     "email": email,
#     "from_page": "detail",
#     "interval": "3d",
#     "goods_info": [
#         # {
#         #     "goods_id": 1064100,
#         #     "cat_id": 3110
#         # },
#         {
#             "goods_id": 1052019,
#             "cat_id": 2
#         }
#     ]
# }

bounce_data = {"client_id": "c25e6fcd-0b9f-4b50-ae66-ca700d0e7519", "country_code": "US",
               "email": email, "from_page": "detail",
               "goods_info": [{"cat_id": 33, "goods_id": 1065870}, {"cat_id": 10, "goods_id": 1064272}],
               "interval": "1d", "language_code": "en"}

list_bounce_data = {"airship_id": "979a2cef-6155-48fa-ae46-12416c512352",
                    "client_id": "C587152A-47CC-4451-B797-0FA39252AD94", "country_code": "CA",
                    "email": email, "from_page": "goods", "cat_id": [3102],
                    "interval": "1d"}


def send_kafka_msg(bounce_data):
    # Create Kafka producer
    conf = {
        'bootstrap.servers': 'nebula03:9092',
        'client.id': 'python-producer'
    }
    producer = Producer(conf)

    # Create test data

    # Send message
    producer.produce(
        'az_bounce_data_v1.test1',
        value=json.dumps(bounce_data).encode('utf-8'),
        callback=delivery_report
    )

    # Wait for message to be delivered
    producer.flush()
    print("Message sent: %s" % json.dumps(bounce_data))


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


if __name__ == "__main__":
    send_kafka_msg(bounce_data)
# @cursor end

import time

import requests
from abandonDate import list_data
from abandonDate import detail_case1, detail_case2, detail_case3,detail_category_list
# ,list_data
from common.handleDatabase import az_db

email_list = [
    # 'test_shiyong1123114041@gaoyaya.com',
    # 'lapuda@gaoyaya.com',
    # 'julie.z@azazie.com',
    # 'mario.wang@gaoyaya.com',
    # 'azfolder4test@gaoyaya.com'
    'shiyong@gaoyaya.com'
]


def sendHomeEmail(home_data, email):
    category = [
        'Bridesmaid Dresses',
        'Wedding Dresses',
        'Mother Of The Bride Dresses', 'Flower Girl Dresses',
        'Formal & Evening', 'Accessories', 'Bridesmaid Dresses,Wedding Dresses,Mother Of The Bride Dresses',
        'Flower Girl Dresses,Formal & Evening,Accessories']
    for item in category:
        sql = f"UPDATE email_extension_by_type set ext_value = '{item}' WHERE email = '{email}'"
        az_db.updateDate(sql)
        print(f'开始发送 home 邮件:', home_data)
        url = 'https://cms-t-4.azazie.com/index.php'
        datas = {
            'method': 'POST',
            'url': 'https://cms-cron-api-t.gaoyaya.com/mail-mock/run-shell?q=1&Authorization=Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84',
            'data[env]': 'cron',
            'data[email]': email,
            'data[scriptId]': '14',
            'data[country]': 'us',
            'data[language]': 'en',
            'data[jsonParams][mail_data][subject]': '占位符，不生效',
            'data[jsonParams][template_data][email]': email,
            'data[jsonParams][template_data][from_page]': 'home',
            'data[jsonParams][template_data][isMock]': True
        }
        params = {
            'q': 'admin/main/mailMock/proxy',
            'Authorization': 'Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84'
        }
        res = requests.post(url, datas, params=params)
        print(res.json())


def sendListEmail(list_data, email):
    print(f'开始发送 list 邮件:', list_data)
    url = 'https://cms-t-4.azazie.com/index.php'
    datas = {
        'method': 'POST',
        'url': 'https://cms-cron-api-t.gaoyaya.com/mail-mock/run-shell?q=1&Authorization=Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84',
        'data[env]': 'cron',
        'data[email]': email,
        'data[scriptId]': '10',
        'data[country]': 'us',
        'data[language]': 'en',
        'data[jsonParams][mail_data][subject]': '占位符，不生效',
        'data[jsonParams][template_data][email]': email,
        'data[jsonParams][template_data][from_page]': 'goods',
        'data[jsonParams][template_data][isMock]': True

    }
    params = {
        'q': 'admin/main/mailMock/proxy',
        'Authorization': 'Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84'
    }

    for cat_id in list_data:
        number = 0
        if type(cat_id) == list:
            for item in cat_id:
                datas[f'data[jsonParams][template_data][cat_id][{number}]'] = item
                number += 1
            res = requests.post(url, data=datas, params=params)
            print(res.json())
            continue
        datas[f'data[jsonParams][template_data][cat_id][{number}]'] = cat_id
        res = requests.post(url, data=datas, params=params)
        print(res.json())


def sendDetailEmail(detail_data, interval, email):
    print(f'开始发送detail {interval} 邮件:', detail_data)
    url = 'https://cms-t-4.azazie.com/index.php'
    datas = {
        'method': 'POST',
        'url': 'https://cms-cron-api-t.gaoyaya.com/mail-mock/run-shell?q=1&Authorization=Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84',
        'data[env]': 'cron',
        'data[email]': email,
        'data[scriptId]': '11',
        'data[country]': 'us',
        'data[language]': 'en',
        'data[jsonParams][mail_data][subject]': '占位符，不生效',
        'data[jsonParams][template_data][email]': email,
        'data[jsonParams][template_data][from_page]': 'detail',
        'data[jsonParams][template_data][interval]': interval,
        'data[jsonParams][template_data][cat_id][0]': 2,
        'data[jsonParams][template_data][cat_id][1]': 7,
        'data[jsonParams][template_data][isMock]': True

    }
    number = 0
    for goods_item in detail_data:
        datas[f'data[jsonParams][template_data][goods_info][{number}][goods_id]'] = goods_item['goods_id']
        datas[f'data[jsonParams][template_data][goods_info][{number}][cat_id]'] = goods_item['cat_id']
        number += 1
    if interval == '1h':
        datas['data[scriptId]'] = '11'
    elif interval == '1d':
        datas['data[scriptId]'] = '12'
    elif interval == '3d':
        datas['data[scriptId]'] = '13'
    params = {
        'q': 'admin/main/mailMock/proxy',
        'Authorization': 'Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84'
    }
    res = requests.post(url, datas, params=params)
    print(res.status_code)
    print('detail邮件发送成功', res.json())


def sendAllCategoryDetailEmail(detail_data, interval, email):
    for category in detail_data:
        sendDetailEmail([category], interval, email)


def sendCaseEmail(email):
    sendDetailEmail(detail_case1, '1h', email)
    sendDetailEmail(detail_case2, '1h', email)
    sendDetailEmail(detail_case3, '1h', email)

    sendDetailEmail(detail_case1, '1d', email)
    sendDetailEmail(detail_case2, '1d', email)
    sendDetailEmail(detail_case3, '1d', email)

    sendDetailEmail(detail_case1, '3d', email)
    sendDetailEmail(detail_case2, '3d', email)
    sendDetailEmail(detail_case3, '3d', email)


if __name__ == '__main__':
    for email in email_list:
        sendCaseEmail(email)

        # sendHomeEmail('test', email)
        # sendListEmail(list_data, email)
        # sendAllCategoryDetailEmail(detail_category_list, '1h', email)
        # sendAllCategoryDetailEmail(detail_category_list, '1d', email)
        # sendAllCategoryDetailEmail(detail_category_list, '3d', email)

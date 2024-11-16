import requests


def sendHomeEmail(home_data):
    pass


def sendListEmail(list_data):
    pass





def sendDetailEmail(detail_data, interval):
    print(f'开始发送detail {interval} 邮件:', detail_data)
    url = 'https://cms-t-4.azazie.com/index.php'
    datas = {
        'method': 'POST',
        'url': 'https://cms-cron-api-t.gaoyaya.com/mail-mock/run-shell?q=1&Authorization=Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84',
        'data[env]': 'cron',
        'data[email]': 'shiyong@gaoyaya.com',
        'data[scriptId]': '11',
        'data[country]': 'us',
        'data[language]': 'en',
        'data[jsonParams][mail_data][subject]': '占位符，不生效',
        'data[jsonParams][template_data][email]': 'shiyong@gaoyaya.com',
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
    params = {
        'q': 'admin/main/mailMock/proxy',
        'Authorization': 'Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84'
    }
    res = requests.post(url, datas, params=params)
    print('detail邮件发送成功', res.json())

category_list = [{
    "goods_id": "1052845",
    "cat_id": "7"
}]
sendDetailEmail(category_list, '1h')

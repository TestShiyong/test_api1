import requests
import re


def erpLogin():
    header = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Upgrade-Insecur"
        "e-Requests": "1",
    }
    url = "http://erp-test.gaoyaya.com:400/admin/privilege.php?_mark=3&act=login&back=%2Fadmin%2Famerican_whs_management%2Fmain_menu.php"
    payload = {
        'username': 'jiayan', 'password': '123456', 'act': 'signin',
        'back': '/admin/american_whs_management/main_menu.php'
    }

    with requests.Session() as session:
        res = session.post(url, data=payload, headers=header)
        token = session.cookies.get_dict()['OKEY']
        print(token)
        return token


def getErpReturnId(token, order_sn):
    key = 'customer_manager/order_edit.php?order_id='

    url = 'http://erp-test.gaoyaya.com:400/admin/american_whs_management/return_apply_list.php?applyStatus=A&roleFlag=customer&orderSnFlag=&orderSn='
    headers = {
        'Cookie': f'OKEY={token}',
        'Origin': 'http://erp-test.gaoyaya.com:400',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://erp-test.gaoyaya.com:400/admin/american_whs_management/return_apply_list.php?applyStatus=A&roleFlag=customer&orderSnFlag=&orderSn='
    }
    data = {
        'applyStatus': 'N',
        'orderSnFlag': 'taobaoOrderSn',
        'orderSn': order_sn,
        'return_to': '0',
        'act': 'inquiry'
    }

    response = requests.post(url, headers=headers, data=data)

    text = response.text
    index = text.find(key)
    if index != -1:
        extracted_text = text[max(0, index - 50):index]
        numbers = re.findall(r'\b\d{7}\b', extracted_text)[0]
        print(numbers)
        return numbers


def approveReturnOrder(token):
    global orders
    for order_sn in orders:
        returnApplyId = getErpReturnId(token, order_sn)
        url = 'http://erp-test.gaoyaya.com:400/admin/american_whs_management/return_apply_list.php?applyStatus=A&roleFlag=customer&orderSnFlag=&orderSn='
        headers = {
            'Cookie': f'OKEY={token}',
            'Origin': 'http://erp-test.gaoyaya.com:400',
            'Upgrade-Insecure-Requests': '1',
        }
        data = {
            'act': 'update',
            'orderSnFlag': 'taobaoOrderSn',
            'orderSn': order_sn,
            'returnOrderSn': '',
            'applyStatus': 'N',
            'returnApplyId': returnApplyId,
            'type': 'A'
        }

        response = requests.post(url, headers=headers, data=data, verify=False)

        print(response.text)


def sendThreeBasket(token):
    url = 'http://erp-test.gaoyaya.com:400/admin/inspinia/warehouse/enter_returned_inventory.php'
    headers = {

        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': f'OKEY={token}',
        'Origin': 'http://erp-test.gaoyaya.com:400',
        'Pragma': 'no-cache',
        'Referer': 'http://erp-test.gaoyaya.com:400/admin/inspinia/warehouse/enter_returned_inventory.php',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data1 = {
        'isLikeNew': '0',
        'isRepair': '0',
        'boxCode': 'shiyong',
        'boxType': 'M',
        'facilityId': '242062559',
        'parentWarehouse': '',
        'act': 'getBoxReturnRKContent'
    }

    data2 = {
        'isLikeNew': '1',
        'isRepair': '0',
        'boxCode': 'shiyong3',
        'boxType': 'M',
        'facilityId': '242062559',
        'parentWarehouse': '',
        'act': 'getBoxReturnRKContent'
    }
    data3 = {
        'isLikeNew': '0',
        'isRepair': '1',
        'boxCode': 'shiyong',
        'boxType': 'M',
        'facilityId': '242062559',
        'parentWarehouse': '',
        'act': 'getBoxReturnRKContent'
    }
    data_list = [data1, data2, data3]
    for data in data_list:
        response = requests.post(url, headers=headers, data=data, verify=False)
        print(response.text)


def unlockBox(token):
    import requests

    url = 'http://erp-test.gaoyaya.com:400/admin/inspinia/warehouse/enter_returned_inventory.php'
    headers = {
        'Cookie': f'OKEY={token}',
        'Origin': 'http://erp-test.gaoyaya.com:400',
        'Pragma': 'no-cache',
        'Referer': 'http://erp-test.gaoyaya.com:400/admin/inspinia/warehouse/enter_returned_inventory.php',
        'X-Requested-With': 'XMLHttpRequest'
    }
    box_list = [('shiyong4', 'repairBoxCode', 'unlockBoxRepair'), ('shiyong3', 'newBoxCode', 'unlockBoxNew'),
                ('shiyong', 'boxCode', 'unlockBox')]
    for box in box_list:
        data = {
            box[1]: box[0],
            'boxType': 'M',
            'act': box[2]
        }

        response = requests.post(url, headers=headers, data=data, verify=False)
        print(response.text)


def getCandidateList():
    url = 'http://erp-test.gaoyaya.com:400/admin/inspinia/warehouse/enter_returned_inventory.php'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': f'OKEY={token}',
        'Origin': 'http://erp-test.gaoyaya.com:400',
        'Pragma': 'no-cache',
        'Referer': 'http://erp-test.gaoyaya.com:400/admin/inspinia/warehouse/enter_returned_inventory.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'boxCode': 'shiyong',
        'orderSn': 'ZZ9776069841',
        'act': 'getAllReturnApply'
    }

    response = requests.post(url, headers=headers, data=data, verify=False)

    print(response.text)
    candidate_list = response.json()['data'][0]['candidate_list']
    return candidate_list

orders = ['ZZ9776069841']
token = erpLogin()
# approveReturnOrder(token)
getCandidateList()

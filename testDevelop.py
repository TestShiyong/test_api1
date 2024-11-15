import requests

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

def getErpOrderDetail(token):
    url = 'http://erp-test.gaoyaya.com:400/admin/american_whs_management/customer_manager/order_edit.php?order_id=86686628'
    headers = {
        'Cookie': f'OKEY={token}',

    }
    res = requests.get(url=url,headers=headers)
    text = res.text
    new_text = text.replace(' ','')
    # print(new_text)
    text_index = new_text.find('az_sn')
    print(new_text[text_index-50:text_index+200])


token = erpLogin()
getErpOrderDetail(token)




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
    url = "http://erp-test.gaoyaya.com:400/admin/privilege.php?_mark=3&act=login&back=%2Fadmin" \
          "%2Famerican_whs_management%2Fmain_menu.php "

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
    headers = {
        'Cookie': f'OKEY={token}',
    }
    result_text = requests.get(url=url, headers=headers).text.replace(' ', '')
    pattern = 'SF\d+'
    matches = re.finditer(pattern, result_text)
    for match in matches:
        print(match.group())

token = erpLogin()
getErpOrderDetail(token)

import requests
import paramiko
import os
import my_path
from bs4 import BeautifulSoup
import re

url = 'https://api-t-1.azazie.com/1.0/user/login'
email = 'shiyong@gaoyaya.com'
pwd = '123456'
order_sn = 'ZZ0700716785'
order_detail_url = f'https://api-t-1.azazie.com/1.0/order/detail?order_sn={order_sn}'


def sendOrderErp(goods_list):
    for i in goods_list:
        params = {
            'hostname': '34.238.212.241',
            'port': 38022,
            'username': 'ec2-user',
            'key_filename': my_path.erp_ft_path,
            'command': f'sudo -u www-data php /var/www/http/zzcms-test1/htm/index.php syncer/syncOne/order_sn/{i}'
            # 要执行的命令
        }
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        hostname = params.get('hostname')
        port = params.get('port', 22)
        username = params.get('username')
        key_filename = params.get('key_filename')
        command = params.get('command')

        try:
            client.connect(hostname, port, username, key_filename=key_filename)
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if output:
                print("Command Output:")
                print(output)
            if error:
                print("Command Error:")
                print(error)

        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH connection failed: {ssh_exception}")
        finally:
            client.close()


def loginErp():
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


def searchErpId(token):
    global order_sn
    url = f'http://erp-test.gaoyaya.com:400/admin/american_whs_management/customer_manager/csmo-inspinia.php?type=search&search_text={order_sn}&search_type=taobao_order_sn'
    headers = {
        'Cookie': f'OKEY={token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_text = response.text
        pattern = r'order_id=(\d+)'
        match = re.search(pattern, response_text)
        if match:
            order_id = match.group(1)
            print("Extracted order_id:", order_id)
            return order_id
        else:
            print("order_id not found in response.text")
    else:
        print('Failed to fetch data. Status code:', response.status_code)


def erpConfirmOrder(order_id, token):
    confirm_order_url = 'http://erp-test.gaoyaya.com:400/admin/american_whs_management/customer_manager/order_edit_action.php'
    headers = {
        'Cookie': f'OKEY={token}',
        'Referer': f'http://erp-test.gaoyaya.com:400/admin/american_whs_management/customer_manager/order_edit.php?order_id={order_id}'

    }
    payload = {
        'track_reason': '1',
        'track_phone': 'Y',
        'actionNote': 'asddfaf',
        'order_action_type_show': '1',
        'sync_type': '1',
        'return_apply_hr': '请选择',
        'order_action_vip_tag': 'Normal',
        'prevent_until': '0',
        'payment_currency': 'USD',
        'order_id': order_id,
        'order_status': '1',
        'shipping_status': '0',
        'shortage_status': '0',
        'shipping_id': '56',
        'action': 'edit_order_status'
    }
    try:
        result = requests.post(url=confirm_order_url, headers=headers, data=payload)
        if result.status_code != 200:
            print('erp confirm 接口响应码不是200 ')

    except:
        print('erp confirm 接口报错')


def erpCreateShip(order_sn, token):
    erp_create_ship_url = 'http://erp-test.gaoyaya.com:400/admin/dev_tools/test_order_shipping.php'
    headers = {
        'Cookie': f'OKEY={token}'
    }
    payload = {
        'submit': '1',
        'taobao_order_sns': order_sn,
        'node': 'SHIPPING',
        'dispatch_assign_provider': '837',
        'container_id': '1884055',
        'location_seq_id': 'zxg12'

    }
    try:
        result = requests.post(url=erp_create_ship_url, data=payload, headers=headers)
        if result.status_code != 200:
            print('创建自动发货任务接口报错 响应码不等于200')

    except Exception as error:
        raise error

def executeRemoteCommand():
    params = {
        'hostname': '16.162.224.248',
        'port': 38022,
        'username': 'azerp',
        'key_filename': my_path.erp_ft_path,
        'command': f'sudo -u www-data php /var/www/http/zzcms-test1/htm/index.php syncer/syncOne/order_sn/{i}'
        # 要执行的命令
    }

if __name__ == '__main__':
    # list1 = ['ZZ2153039929', 'ZZ7769416288', 'ZZ3961700579', 'ZZ5694050892', 'ZZ5589869843', 'ZZ3300542899']
    # execute_remote_command(params)
    # token = loginAZ()
    # order_id = getOrderId(token)

    cookie = loginErp()
    erp_order_id = searchErpId(cookie)
    erpConfirmOrder(erp_order_id, cookie)
    erpCreateShip(order_sn, cookie)

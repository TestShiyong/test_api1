import requests
import paramiko
import os
import myPath
from bs4 import BeautifulSoup
import re


def sendOrderErp(goods_list):
    for i in goods_list:
        params = {
            'hostname': '34.238.212.241',
            'port': 38022,
            'username': 'ec2-user',
            'key_filename': myPath.erp_ft_path,
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


def getErpOrderId(token):
    global orders
    erp_order_list = []
    for order_sn in orders:
        url = f'http://erp-test.gaoyaya.com:400/admin/american_whs_management/customer_manager/csmo-inspinia.php?' \
              f'type=search&search_text={order_sn}&search_type=taobao_order_sn&order_type_showroom=-1' \
              f'&show_orders%5B%5D=customer_orders&show_orders%5B%5D=test_orders&order_status=-1'
        headers = {
            'Cookie': f'OKEY={token}',

        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_text = response.text
            pattern = r'order_id=(\d+)'
            match = re.search(pattern, response_text)
            if match:
                order_id = match.group(1)
                print("Extracted order_id:", order_id)
                erp_order_list.append(order_id)
            else:
                print(f"order_id not found in response.text,order_sn:{order_sn}")
        else:
            print('Failed to fetch data. Status code:', response.status_code)
    print('confirmErpOrderList:', erp_order_list)
    return erp_order_list


def erpConfirmOrder(erp_order_id_list, token, payment_currency='USD'):
    if not erp_order_id_list:
        print('erp order_id is none')
        return
    for order_id in erp_order_id_list:
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
            'payment_currency': payment_currency,
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


def createShippingTask(token):
    global orders
    for order_sn in orders:
        erp_create_shipping_url = 'http://erp-test.gaoyaya.com:400/admin/dev_tools/test_order_shipping.php'
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
            result = requests.post(url=erp_create_shipping_url, data=payload, headers=headers)
            if result.status_code != 200:
                print('创建自动发货任务接口报错 响应码不等于200')

        except Exception as error:
            raise error


def getShippingTaskId(token):
    global orders
    shipping_taskid_list = []
    for shipping_order_sn in orders:

        get_shipping_task_url = 'http://erp-test.gaoyaya.com:400/admin/dev_tools/test_order_shipping.php'
        headers = {
            'Cookie': f'OKEY={token}'
        }
        result = requests.get(url=get_shipping_task_url, headers=headers)
        text = result.text

        index = text.find(shipping_order_sn)
        if index != -1:
            extracted_text = text[max(0, index - 100):index]
            numbers = re.findall(r'\b\d{4}\b', extracted_text)[0]
            shipping_taskid_list.append(numbers)
    print('shippingTaskidList:', shipping_taskid_list)
    return shipping_taskid_list


def executeErpRemoteCommand(params):
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


def shipOrder(token):
    sum = 0
    shipping_task_id = getShippingTaskId(token)

    for shipping_id in shipping_task_id:
        sum += 1
        print(f'开始执行job,执行次数：{sum}')
        params = {
            'hostname': '16.162.224.248',
            'port': 38022,
            'username': 'azerp',
            'key_filename': myPath.erp_aws_path,
            'command': f'sudo php /var/www/http/erp400/azpublic/index.php /cli/OrderFastDelivery/executeCrontab/{shipping_id}'
            # 要执行的命令
        }
        executeErpRemoteCommand(params)


def syncOrderToAZ():
    global orders
    for az_order_sn in orders:
        url = 'http://azscript.test.com:400/admin/zz_order_action.php'
        payload = {'taobao_order_sn': az_order_sn, 'single': '1', 'port': '400'}
        requests.post(url=url, data=payload)
        print(f'{az_order_sn}已同步到网站')


def createSampleBookingItem():
    params = {
        'hostname': '16.162.224.248',
        'port': 38022,
        'username': 'azerp',
        'key_filename': myPath.erp_aws_path,
        'command': 'php /var/www/http/erp405/protected/yiic azReserveOrderInventory createAzReserveRecord'
        # 要执行的命令
    }
    executeErpRemoteCommand(params)


def deliveryOrder(token):
    status_list = ['attempt_deliver', 'shipping_signed']
    global orders
    for order_sn in orders:
        for status in status_list:
            url = 'http://erp-test.gaoyaya.com:400/admin/american_whs_management/tools/mock_tracking.php'
            data = {
                'category': status,
                'taobao_order_sn': order_sn,
                'act': 'add'
            }
            headers = {
                'Cookie': f'OKEY={token}'
            }
            requests.post(url=url, data=data, headers=headers)
            print(f'{order_sn}更新状态 （{status}）')


#
# def


if __name__ == '__main__':
    # orders = []
    orders = ['ZZ3073874828', 'ZZ7580171652', 'ZZ0698767511']
    sendOrderErp(orders)
    token = erpLogin()
    erp_id_list = getErpOrderId(token)
    erpConfirmOrder(erp_id_list, token)
    createShippingTask(token)
    shipOrder(token)
    # deliveryOrder(token)
    syncOrderToAZ()

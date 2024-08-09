"""
@Project : new_api
@File    : send_request
@Author  : Shi yong 
@Data    : 2022/3/5
request模块 二次封装
"""

import requests

from common.handleLog import log


def sendRequest(method: str, url: str, country=None, data=None, token=None, output=True):
    """
    所有接口调用都要此方法 经过以下处理
        token 为默认参数 判断是否传 token 如果传token 就通过字典 把token值加入请求头添加字段值
        method:判断 传什么请求方式 调用什么方式接口
        url:拼接处理 如果传非完整路径就自动拼接
        data:1.字符串转字典处理 2.如果data字符串中 含 null（非python数据类型）则替换为None
        调用接口是 日志输出 请求方式 url  data header 接口响应值  接口响应code
    header
    :param
    :param
    :param
    :return:
    """

    # 请求方式大写处理
    method = method.upper()

    # ulr 拼接处理
    base_url = 'https://apix-p3.azazie.com/1.0'
    if url.startswith('/'):
        url = base_url + url

    # 判断data是否为字符串  转为字典
    if data is not None and isinstance(data, str):
        if data.find('null') != -1:
            data.replace('null', 'None')
            return eval(data)
    # 获取header
    header = getHeader(token, country)

    # 调用请求 输出log
    log.info("请求头为：{}".format(header))
    log.info("请求方法为：{}".format(method))
    log.info("请求url为：{}".format(url))
    log.info("请求数据为：{}".format(data))

    if method == 'GET':
        if url == 'http://127.0.0.1:8899/money':
            return None
        res = requests.get(url, headers=header)
        log.info("响应状态码为：{}".format(res.status_code))
        if output:
            log.info("响应数据为：{}".format(res.json()))
        return res

    elif method == 'POST':
        res = requests.post(url, json=data, headers=header)
        log.info("响应状态码为：{}".format(res.status_code))
        if output:
            log.info("响应数据为：{}".format(res.json()))
        return res

    elif method == 'DELETE':
        res = requests.delete(url, json=data, headers=header)
        log.info("响应状态码为：{}".format(res.status_code))
        if output:
            log.info("响应数据为：{}".format(res.json()))
        return res
    elif method == 'PUT':
        res = requests.put(url, json=data, headers=header)
        log.info("响应状态码为：{}".format(res.status_code))
        if output:
            log.info("响应数据为：{}".format(res.json()))
        return res


def getHeader(token=None, country=None):
    header = {"Content-Type": "application/json",
              "Accept": "application/json",
              "x-app": "pc",
              "x-token": "",
              "x-project": "azazie",
              "x-countryCode": "US",
              "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
              }
    if token:
        header["x-token"] = token
    if country:
        header['x-countryCode'] = country
    return header

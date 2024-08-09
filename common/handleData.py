"""
@Project : new_api
@File    : handle_data
@Author  : Shi yong 
@Data    : 2022/3/5
处理接口数据替换
"""
from jsonpath import jsonpath
import re

from common.handleLog import log
from common.handleConfig import cf


class GlobalData:
    pass


def clearGlobalVar():
    """
       清除用例要使用到的数据。
       """
    value = dict(GlobalData.__dict__.items())
    for key, value in value.items():
        if key.startswith("__"):
            pass
        else:
            delattr(GlobalData, key)


def extract(extract_data, response):
    """
    根据jsonpath提取表达式，从响应结果当中，提取数据并设置为环境变量EnvData类的类属性，作为全局变量使用。
    :param extract_data: 从excel当中读取出来的，提取表达式的字符串。
    :param response: http请求之后的响应结果。
    :return:Nonoe
    """
    log.info('开始提取数据,提取表达式为{}'.format(extract_data))

    dict_extract_data = eval(extract_data)
    for key, value in dict_extract_data.items():
        res = jsonpath(response, value)[0]

        log.info('提取数据成功：{}'.format(res))

        setattr(GlobalData, key, res)


def replaceAllData(case: dict):
    """
    便利用例中的值 调用数据获取替换方法返回替换后的值 再把替换后的值替换到用例内

    :param case:
    :return:
    """

    log.info("开始替换数据，替换前的数据为:{}".format(case))

    # 便利用例
    for key, value in case.items():
        # 如果 value是字符串不为空 就调用数据查找替换方法替换数据并返回
        if value is not None and isinstance(value, str):
            # 把替换后的值  替换进用例
            case[key] = __replaceData(value)

    log.info("替换数据完成，替换后的数据为:{}".format(case))

    return case


def __replaceData(data: str):
    """
    提取用例中的关键字 通过关键字去全局变量中 或 配置文件中查找并替换  可以替换多个关键字
    处理步骤
        用例中的值有多个参数需要替换 用正则表达式提取出来 放进列表


    :param data: 用例中替换前的值
    :return: 用例替换后的值
    """
    # 用例中的值有多个参数需要替换 用正则表达式提取出来 放进列表
    result = re.findall("#(.*?)#", data)
    if result:
        # 便利关键字列表
        for item in result:
            try:
                # 配置文件中获取值
                value = cf.getStr('Account', item)
            except:
                try:
                    # 配置文件查找不到 全局变量中查找 获取值
                    value = getattr(GlobalData, item)
                except:
                    continue
            # 把用例中的关键字 替换成查询到的参数
            data.replace(item, value)
    return data


def replaceData(case: dict, old_data, new_data):
    """
    替换用例中value中的值  一个值中 只能替换一个关键字

    :param case: 单条测试用例 字典类型
    :param old_data: 被替换的参数
    :param new_data: 将要替换的参数
    :return: 替换后的参数
    """
    for key, value in case.items():
        if value is not None and isinstance(value, str):
            if value.find(old_data) != -1:
                case[key] = value.replace(old_data, new_data)
    return case

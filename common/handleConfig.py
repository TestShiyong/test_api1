"""
@Project : new_api
@File    : red_conf_file
@Author  : Shi yong 
@Data    : 2022/3/5

二次封装的读取配置文件类 用于读取配置文件中的参数 作为参数返回
"""

from configparser import ConfigParser

import myPath


class ConfigReader:

    @staticmethod
    def getStr(item, key):
        config_parser = ConfigParser()
        config_parser.read(myPath.configFilePath)
        return config_parser.get(item, key)

    @staticmethod
    def getInt(item, key):
        config_parser = ConfigParser()
        config_parser.read(myPath.configFilePath)
        return config_parser.getint(item, key)

    @staticmethod
    def getFlout(item, key):
        config_parser = ConfigParser()
        config_parser.read(myPath.configFilePath)
        return config_parser.getfloat(item, key)

    @staticmethod
    def getBoolean(item, key):
        config_parser = ConfigParser()
        config_parser.read(myPath.configFilePath)
        return config_parser.getboolean(item, key)


if __name__ == '__main__':
    ConfigReader.getStr(myPath.cf_path)

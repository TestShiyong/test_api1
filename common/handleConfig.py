"""
@Project : new_api
@File    : red_conf_file
@Author  : Shi yong 
@Data    : 2022/3/5

二次封装的读取配置文件类 用于读取配置文件中的参数 作为参数返回
"""

from configparser import ConfigParser

import myPath


class ReadConfigFile:
    def __init__(self, file_path):
        """

        :param file_path:
        """
        self.new_config_parser = ConfigParser()
        self.new_config_parser.read(file_path)

    def getStr(self, item, key):
        return self.new_config_parser.get(item, key)

    def getInt(self, item, key):
        return self.new_config_parser.getint(item, key)

    def getFlout(self, item, key):
        return self.new_config_parser.getfloat(item, key)

    def getBoolean(self, item, key):
        return self.new_config_parser.getboolean(item, key)


cf = ReadConfigFile(myPath.cf_path)
if __name__ == '__main__':
    print(cf.getStr('Host', 'host'))
    cf = ReadConfigFile(myPath.cf_path)

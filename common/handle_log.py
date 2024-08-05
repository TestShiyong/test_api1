"""
@Project : new_api
@File    : log
@Author  : Shi yong 
@Data    : 2022/3/3

二次封装的logger类   把log输出到控制台 和 文件里面
s"""

import logging
import myPath


class Log(logging.Logger):
    def __init__(self, log_name, level=logging.DEBUG, file=None):
        """

        log创建收集器 getLogger
        设置收集级别 log.setLevel(logger.INFO)

        设置日志格式 format=logger.Format 独立类
        创建渠道 handle=logger.StreamHandler
        渠道绑定格式 handle.setFormat(format)

        收集器添加渠道 self.addHandle(handle)
        :param log_name:log_name
        :param level:日志级别
        :param file:文件路径
        """
        super().__init__(log_name,level)
        # 创建日志格式
        fmt = '%(name)s:%(asctime)s:%(funcName)s:%(filename)s:%(lineno)d:%(levelname)s:%(message)s'
        # 设置日志格式
        formats = logging.Formatter(fmt)
        # 创建console收集渠道
        handle1 = logging.StreamHandler()
        # 渠道绑定日志格式
        handle1.setFormatter(formats)
        # 渠道添加入收集器
        self.addHandler(handle1)

        if file:
            file_handle=logging.FileHandler(file,mode='a', encoding='utf-8')
            file_handle.setFormatter(formats)
            self.addHandler(file_handle)


log = Log('Azazie',file=my_path.log_path+'\\my_log.log')


if __name__ == '__main__':
    new_log=Log('Azazie',file=my_path.log_path+'\\my_log.log')
    new_log.warning('输出log test111')
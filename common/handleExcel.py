"""
@Project : new_api
@File    : excel1
@Author  : Shi yong 
@Data    : 2022/3/3
"""
"""封装的读取excel 返回测试数据类"""


from openpyxl import load_workbook
import path
import myPath


class Excel:

    def __init__(self, file_path,sheet):
        """
        :param file_path:传入excel文件路径
        """
        form_data = load_workbook(file_path)
        self.data = form_data[sheet]

    def redTitle(self):
        """
        获取excel首行数据
        :return: 返回excel首行数据值 装入列表内
        """
        list_title = []
        for i in list(self.data.rows)[0]:
            list_title.append(i.value)
        return list_title

    def allData(self):
        """
        便利excel除首行外的所有行
        再便利每一行取值添加进列表，单行添加完成使用zip把 首行数据 +当前行数据拼接成字典 添加进列表
        便利完所有行后 返回列表包字典数据

        :return:返回列表包字典数据
        """
        all_list = []
        for items in list(self.data.rows)[1:]:
            row_list = []
            for item in items:
                row_list.append(item.value)
            all_list.append(dict(zip(self.redTitle(), row_list)))

        return all_list


if __name__ == '__main__':
    aa = Excel(myPath.data_path + '\\register.xlsx','register_form')
    print(aa.redTitle())
    print(aa.allData())

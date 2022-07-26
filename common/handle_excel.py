"""
@Project : new_api
@File    : excel1
@Author  : Shi yong 
@Data    : 2022/3/3
"""
"""封装的读取excel 返回测试数据类"""


from openpyxl import load_workbook
import path
import my_path


class Excel:

    def __init__(self, file_path):
        """
        :param file_path:传入excel文件路径
        """
        form_data = load_workbook(my_path.data_path + '\\register.xlsx')
        self.data = form_data['register_form']
        print(list(self.data))

    def red_title(self):
        """
        获取excel首行数据
        :return: 返回excel首行数据值 装入列表内
        """
        list_title = []
        for i in list(self.data.rows)[0]:
            list_title.append(i.value)
        return list_title

    def all_data(self):
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
            all_list.append(dict(zip(self.red_title(), row_list)))
        return all_list


if __name__ == '__main__':
    aa = Excel(my_path.data_path + '\\register.xlsx')
    print(aa.red_title())
    print(aa.all_data())

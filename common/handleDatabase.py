"""
@Project : new_api
@File    : database
@Author  : Shi yong 
@Data    : 2022/3/4

数据库二次封装类
"""

import pymysql


class Database:

    def __init__(self, user, password, host, port, database):
        """

        :param user:
        :param password:
        :param host:
        :param port:
        """
        self.connect = pymysql.connect(
            user=user,
            password=password,
            host=host,
            database=database,
            port=port,
            charset='utf8',
        )
        self.cur = self.connect.cursor(pymysql.cursors.DictCursor)

    def getFetchall(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def getFetchone(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()

    def updateDate(self, sql):
        count_line = self.cur.execute(sql)
        print('修改成功 受影响行数：{}'.format(count_line))
        self.connect.commit()
        return count_line

    def closeConnect(self):
        self.cur.close()
        self.connect.close()

az_db = Database(
    user='azazie',
    password='azazie',
    host='az-test-db.gaoyaya.com',
    port=3306,
    database='azazie'

)


if __name__ == '__main__':
    az_db = Database(
        user='azazie',
        password='azazie',
        host='az-test-db.gaoyaya.com',
        port=3306,
        database='azazie'

    )
    # sql = "UPDATE email_extension_by_type set ext_value = 'Bridesmaid Dresses' WHERE email = 'test_shiyong1118@gaoyaya.com' "
    #
    # az_db.updateDate(sql)

#
# bi = Database(
#     user='az_query',
#     password='az_query',
#     host='report-system.cbb0nles4v8i.us-east-1.rds.amazonaws.com',
#     port=3306,
#     database='nebulas')


# if __name__ == '__main__':
#
#
#     aa = db.getFetchall('SELECT * FROM `style`')
#     print(aa)
#     list1 = []
#     for i in aa:
#         list1.append({"style_id": i['style_id'], "value": i['value']})
#     print(list1)

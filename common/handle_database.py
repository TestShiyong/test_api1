"""
@Project : new_api
@File    : database
@Author  : Shi yong 
@Data    : 2022/3/4

数据库二次封装类
"""

import pymysql


class Database:

    def __init__(self, user, password, host, port=3306, database='table_one'):
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

    def get_fetchall(self, sq):

        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_fetchone(self, sq):
        self.cur.execute(sql)
        return self.cur.fetchone()

    def alter_data(self,sq):
        count_line = self.cur.execute(sql)
        print('修改成功 受影响行数：{}'.format(count_line))
        self.connect.commit()
        return count_line

    def close_connect(self):
        self.cur.close()
        self.connect.close()
if __name__ == '__main__':


    db = Database(
        user='root',
        password='shi1557225637_',
        host='rm-uf60nj0t33i3601vx3o.mysql.rds.aliyuncs.com'

    )
    sql='UPDATE  student  SET  Ssex=\'神\' WHERE  Sname=\'赵雷\''

    db.get_fetchall(sql)

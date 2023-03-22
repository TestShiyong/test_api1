#:@ TIME 2021/10/24   18:52
#:@FILE  handle_new_email.py
#:@EMAIL  1557225637@QQ.COM
import random
from common.handle_database import Database


# 获取手机号


def creat_phone():
    header_list = [135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188, 198]
    title = random.randint(0, len(header_list) - 1)
    header_phone = str(header_list[title])
    for _ in range(0, 8):
        header_phone += str(random.randint(0, 9))
    return header_phone




def get_NewPhone():
    db = Database()
    while True:
        phone = creat_phone()
        sq = "select * From users  where  PHONE={}".format(phone)
        if db.count_line(sq) == 0:
            db.close_db()
            return phone


phone = get_NewPhone()
print(phone)


def get_new_emai():
    new_email = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8))
    return new_email

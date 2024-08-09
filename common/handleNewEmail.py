#:@ TIME 2021/10/24   18:52
#:@FILE  handleNewEmail.py
#:@EMAIL  1557225637@QQ.COM
import random
from common.handleDatabase import Database


# 获取手机号
def creatPhone():
    header_list = [135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188, 198]
    title = random.randint(0, len(header_list) - 1)
    header_phone = str(header_list[title])
    for _ in range(0, 8):
        header_phone += str(random.randint(0, 9))
    return header_phone


def getNewPhone():
    db = Database()
    while True:
        phone = creatPhone()
        sq = "select * From users  where  PHONE={}".format(phone)
        if db.count_line(sq) == 0:
            db.close_db()
            return phone


phone = getNewPhone()
print(phone)


def newEmai():
    new_email = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8))
    return new_email

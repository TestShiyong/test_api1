#:@ TIME 2021/10/25   20:19
#:@FILE  myApi.py
#:@EMAIL  1557225637@QQ.COM

from flask import Flask, request
import json
import time
from common.handleDatabase import Database

# db=Database()


sever = Flask(__name__)


@sever.route('/money', methods=['POST'])
def MyApi():
    password = (request.form.get('password'))
    phone = (request.form.get('phone'))
    money = (request.values.get('money'))

    if phone and password and money:
        try:
            phone = int(phone)
        except ValueError:
            msg = {"code": 401, "msg": " phone type not int"}
            return json.dumps(msg)

        str_phone = len(str(phone))
        if str_phone > 11:
            msg = {"code": 402, "msg": " phone leng not >11"}
            return json.dumps(msg)

        elif str_phone < 11:
            msg = {"code": 403, "msg": " phone leng not <11"}
            return json.dumps(msg)

        try:
            money = float(money)
        except ValueError:
            msg = {"code": 404, "msg": " money type not int or float"}
            return json.dumps(msg)

        cc = str(money)
        c = cc.find('.')
        d = cc[c + 1:]
        if len(d) > 2:
            msg = {"code": 405, "msg": "You can't have more than two decimal places"}
            return json.dumps(msg)

        # sq='SELECT * FROM users WHERE PHONE="{}" AND PASSWORD ="{}"'.format(str(phone),str(password))
        # res=db.get_fetchone(sq)
        # if res:
        #     money1=float(res['MONEY'])
        #     money1+=money
        #
        #     sq2='UPDATE users set MONEY ="{}" WHERE PHONE=16628554195'.format(money1)
        #     db.get_fetchone(sq2)
        #     db.commit()
        #     new_money=round(money1,2)
        #     res = {"code": 0, "msg": "success", "money": new_money}
        #     return res
        res = {"code": 0, "msg": "success", "money": 9999}
        time.sleep(0.1)
        return res
        # else:
        #     res={"code":406,"msg":"The account or password is incorrect"}
        #     return res
    else:
        res = {"code": 407, "msg": "Wrong argument"}
        return res


sever.run(port=8899, debug=True)

import requests


# header = {"Content-Type": "application/json",
#           "Accept": "application/json",
#           "x-app": "pc",
#           "x-token": "",
#           "x-project": "azazie",
#           "x-countryCode": "US",
#           "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
#           }

def lego_login():
    url = 'https://api-t-1-lego.azazie.com/auth/login'
    datas = {"username": "admin", "password": "lb123456"}
    res = requests.post(url, json=datas)
    token = res.json()['data']['token']
    return token


def get_languagecode_value(token, code, languageCode, ):
    url = 'https://api-lego.azazie.com/config/multilanguage/get?keyWords=&code=payment_method_not_supported&languageCode=en&currentPage=1&curPageSize=50'
    header = {"Token": token}

    datas = {"keyWords": "",
             "code": code,
             "languageCode": languageCode,
             "currentPage": "1",
             "curPageSize": "50",
             }

    res = requests.get(url, json=datas, headers=header)
    value = res.json()['data']['list'][0]
    aa = ['code','en','de','fr','es','it','nl']
    for k,v in value.items():
        if k in aa:
            print(k,':',v)
            print()
    print()
    print()





token = lego_login()
list_codes = ['	page_review_confirm_note','page_help_menu_return_policy','page_common_and','page_checkout_dye_lot_faq']


def codes(list_codes, languageCode):
    for code in list_codes:
        get_languagecode_value(token, code, languageCode)


codes(list_codes,'en')
lego_login()






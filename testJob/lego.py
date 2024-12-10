import requests


# header = {"Content-Type": "application/json",
#           "Accept": "application/json",
#           "x-app": "pc",
#           "x-token": "",
#           "x-project": "azazie",
#           "x-countryCode": "US",
#           "authorization": "Basic bGViYmF5OnBhc3N3MHJk"
#           }

def legoLogin():
    url = 'https://api-t-1-lego.azazie.com/auth/login'
    datas = {"username": "admin", "password": "lb123456"}
    res = requests.post(url, json=datas)
    token = res.json()['data']['token']
    return token


if __name__ == '__main__':
    # token = legoLogin()

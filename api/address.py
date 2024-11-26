import requests
from api.apiOrder import login

BASE_URL = 'https://api-t-1.azazie.com'

# BASE_URL = 'https://apix.azazie.com'
email = 'shiyong@gaoyaya.com'
password = '123456'


def fetchState():
    url = BASE_URL + '/1.0/address-suggest/fetch-sub-region'

    param_date = {
        'order_country_code': 'us',
        'ff_id': '3859'
    }
    res = requests.post(url, params=param_date)
    state_item_list = res.json()['data']['res']['ffRegionList']
    state_list = []
    for state_item in state_item_list:
        region_ame = state_item['regionName']
        region_id = state_item['ffRegionId']
        state_list.append({'region_ame': region_ame, 'region_id': region_id})
    print(state_list)

    return state_list


def fetchCity(token):
    url = "https://p2.azazie.com/pre/1.0/address-suggest/fetch-sub-region?order_country_code=US&ff_id=3861"

    param_date = {
        'order_country_code': 'us',
        'ff_id': 3863
    }
    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie',
        'x-token': token
    }
    res = requests.post(url,headers=headers)
    city_item_dict = res.json()['data']['res']['zipCodeMap']
    city_list = []
    for k,v in city_item_dict.items():
        city_list.append(k,v)
        print(k,v)
    # print(state_list)
    return city_list


if __name__ == '__main__':
    token = login(email, password)
    # fetchState()
    fetchCity(token)
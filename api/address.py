import requests
from api.azApi import login
import random

# BASE_URL = 'https://api-t-1.azazie.com'

BASE_URL = 'https://apix.azazie.com'
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

    return state_list


def fetchCityAndZipcode(province, token):
    url = f"https://p2.azazie.com/pre/1.0/address-suggest/fetch-sub-region?order_country_code=US&ff_id={province}"

    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie',
        'x-token': token
    }
    res = requests.post(url, headers=headers)
    city_item_list = res.json()['data']['res']['ffRegionList']
    if len(city_item_list) > 11:
        city_item_list = random.sample(res.json()['data']['res']['ffRegionList'], 10)

    if city_item_list:
        city_list = []
        for city_item in city_item_list:
            city_list.append((city_item['regionName'], city_item['ffRegionId'], city_item['zipCodeList'][0]))
        return city_list
    else:
        return None


def editAddress(province, province_text, city, zipcode, token):
    url = 'https://p2.azazie.com/pre/1.0/address/edit'
    address_datas = {"address_type": 1, "country": 3859, "province": province, "province_text": province_text,
                     "city": city, "city_text": "Dpo", "district": 0, "district_text": "",
                     "address": "123 Main Street", "sign_building": "", "zipcode": zipcode, "check_validation": 0,
                     "first_name": "shi3", "last_name": "Yong3", "tel": "1245818285", "sort_by": "addressId",
                     "address_id": 16007644, "is_default": 0}

    headers = {
        'x-app': 'pc',
        'x-countrycode': 'US',
        'x-languagecode': 'en',
        'x-original-uri': '',
        'x-project': 'azazie',
        'x-token': token
    }
    res = requests.post(url, json=address_datas, headers=headers)
    print(province_text, province, city, zipcode)
    code = res.status_code
    if code != 200:
        print('error 地址异常 ------------------------------------------------------------------',address_datas)


if __name__ == '__main__':
    token = login(email, password)
    state_list = fetchState()
    for state_items in state_list:
        province = state_items['region_id']
        province_text = state_items['region_ame']
        city_zipcode_list = fetchCityAndZipcode(province, token)
        if city_zipcode_list:
            for city_zipcode in city_zipcode_list:
                city = city_zipcode[1]
                zipcode = city_zipcode[2]
                editAddress(province, province_text, city, zipcode, token)
                print('test')
        else:
            continue

    # fetchCityAndZipcode(3921,token)

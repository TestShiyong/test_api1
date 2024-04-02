import requests

url = 'https://apix-p5.azazie.com/1.0/product/sample-info'
headers = {'Content-Type': 'application/json', 'x-app': 'pc', 'x-token': '', 'x-project': 'azazie',
           'x-countryCode': 'US', 'x-languagecode': 'en'}
data = {"goods_name": "", "goods_id": 8888888, "cat_id": 2}
res = requests.get(url, params=data, headers=headers)

print(res.json())
print(res.status_code)

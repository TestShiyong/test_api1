import requests

url = 'https://apix-p.azazie.com/1.0/list/content?cat_name=&dress_type=dress&page=1&limit=48&sort_by=popularity'
headers = {'Content-Type': 'application/json', 'x-app': 'pc', 'x-token': '', 'x-project': 'azazie',
           'x-countryCode': 'US', 'x-languageCode': 'en', 'user_agent': 'azbot'}
data = {'filters': {}, 'is_plus_size': False, 'in_stock': False, 'from_style_quiz': False, 'quiz_progress': '',
        'view_mode': []}
res = requests.post(url, json=data, headers=headers)
print(res.status_code)

import requests

url = 'https://cms-t-4.azazie.com/index.php'
data = {
    'method': 'POST',
    'url': 'https://cms-cron-api-t.gaoyaya.com/mail-mock/run-shell?q=1&Authorization=Bearer FbVKVHJYbZ5QZMeKd9CoRx8Z7eywGx84',
    'data[env]': 'cron',
    'data[email]': '',
    'data[scriptId]': '',
    '': '',
'': '',
'': '',
'': '',
'': '',
'': '',
}
res = requests.post(url, )

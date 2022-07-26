

# 列表推导式
list1 = [i for i in range(10)]
print(list1)

# 判断 列表推导式
list2 = [i for i in range(10) if i % 2 != 0]
print(list2)

# 双层循环 推导式
list3 = [(i, j * 5) for i in 'abcdef' for j in range(5)]
print(list3)

# 字典推导式
'获取字典中的key是小写的键值对'
dict1 = {"a": 10, "B": 20, "C": True, "D": "hello world", "e": "python教程"}
dict1 = {key: dict1.get(key) for key, value in dict1.items() if key.islower()}
print(dict1)

'将字典里的所有key设置为小写'
dict2 = {"a": 10, "B": 20, "C": True, "D": "hello world", "e": "python教程"}
dict2 = {key.lower(): value for key, value in dict2.items()}
print(dict2)

"将字典内 所有key为小写字母的 value赋值为error"
dict3 = {"a": 10, "B": 20, "C": True, "D": "hello world", "e": "python教程"}
dict3 = {key: value if key.islower() else 'error' for key, value in dict3.items()}
print(dict3)


'将cookie 字符串修改成字典'
cookies = "anonymid=jy0ui55o-u6f6zd; depovince=GW; _r01_=1; JSESSIONID=abcMktGLRGjLtdhBk7OVw;" \
          " ick_login=a9b557b8-8138-4e9d-8601-de7b2a633f80; _ga=GA1.2.1307141854.1562980962;" \
          " _gid=GA1.2.201589596.1562980962; _c1=-100; first_login_flag=1; ln_uact=18323008898"

dict4 = {i.split('=')[0]: i.split('=')[1] for i in cookies.split(';')}
print(dict4)
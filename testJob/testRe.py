import re

text = '<optionid="az_sn">SF17662</option><optionid="az_sn">AZ68005431</option><optionid="az_sn">AZ93851590</option>'

pattern  = 'SF\d+'
matches = re.finditer(pattern,text)
for match in matches:
    print(match.group())  # 输出匹配到的内容

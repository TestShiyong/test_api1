# q清空文件 写入一行文件
import csv

with open('test_file/111.txt', mode='wt', encoding='utf-8') as f:
    f.write('shiuong')

# 读取文件所有内容
with open('test_file/222.txt', mode='rt', encoding='utf-8') as f1:
    print(f1.read())

# 读取图片二进制编码，读的原始二进制 不存在编码
with open('test_file/az.png', mode='rb') as f2:
    content = f2.read()
    f2.close()
# 写入读取到的 文件读的原始二进制 不存在编码
with open('test_file/az2.png', mode='wb') as f3:
    f3.write(content)

print('------------------------------------------------------------------------------------------------------')

# 多用户注册写入
"""

file_obj = open('test_file/info.txt', mode='wt', encoding='utf-8')
while True:
    name = input('enter name:')
    if name.upper() == 'Q':
        break
    age = input('enter age:')

    data = '{}:{}\n'.format(name, age)
    # 并未理解写入文件  只是写到了缓冲区
    file_obj.write(data)
    # 立即写入到文件
    file_obj.flush()
file_obj.close()


"""

"""

# 末尾追加

file_obj = open('test_file/info.txt', mode='a+', encoding='utf-8')
while True:
    name = input('enter name:')
    if name.upper() == 'Q':
        break
    age = input('enter age:')

    data = '{}:{}\n'.format(name, age)
file_obj.close()
"""

"""
#遍历所有行
open_obj = open('test_file/info.txt', mode='r+', encoding='utf-8')
for i in open_obj:
    print(open_obj.readline().strip())

"""

"""
文件 数据替换

with open('test_file/replase.txt', mode='r+', encoding='utf-8') as f1, open('test_file/replase2.txt', mode='w+',
                                                                            encoding='utf-8') as f2:
    for i in f1:
        new_line =i.replace('三', '3')
        f2.write(new_line)
    f2.seek(0)
    print(f2.read())
    
    
"""
import csv
def writer_csv_demo2():
    headers = ["name", "age", "height"]
    values = [
        {"name":"王11","age":18,"height":178},
        {"name":"王22","age":18,"height":178},
        {"name":"王33","age":18,"height":178}
    ]
    with open("test_file/aa.csv","w", encoding="utf-8",newline="") as fp: #newline=""去掉两行之间的空行
        writer = csv.DictWriter(fp,headers) # 使用csv.DictWriter()方法，需传入两个个参数，第一个为对象，第二个为文件的title
        writer.writeheader()  # 使用此方法，写入表头
        writer.writerows(values) #写入多行，每一行是一个字格式的数据

writer_csv_demo2()


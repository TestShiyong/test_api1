
"""
生成器
"""
# a = (i for i in range(1, 101))
# print(next(a))
# print(next(a))
#
# # yield 返回生成器对象 每用next取一次值就返回下一个值  取完再取会报错
# def gen_fun():
#     yield [i for i in range(10)]
#     print('hellow  python')
#     yield 200
#     yield 300
#
#         # 返回生成器对象
# gen_obj = gen_fun()
# print(gen_obj)
# print(next(gen_obj))
# print(next(gen_obj))
# print(next(gen_obj))







"""
迭代器
"""
# iter 把可迭代对象转换成 迭代器
a=[ i for i in range(10)]
print(a)
b=iter(a)
print(next(b))
print(next(b))

# 可迭代对象和迭代器的区别
'可迭代对象 内部实现了__iter__方法,迭代器内部除了iter方法外 还实现了next方法'
'生成器是迭代器的一种 ，生成器器 和迭代器都可进行迭代'
'生成器内部还实现了 send方法 可与生成器进行交互'
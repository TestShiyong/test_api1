# '''
# filter
# '''
#
#
# def fun(n):
#     return isinstance(n, str)
#
#
# list1 = [1, 2, 657, 78, 'a', 'adssa']
#
# res = filter(fun, list1)
# print(res)
# print(list(res))
#
# '''
# map
# '''
#
# def func(n):
#     if isinstance(n, str):
#         return 1000
#     else:
#         return 9
#
#
# list2 = [1, 2, 3, 4, 'ad', 'dawd', False]
# response = map(func, list2)
# print(list(response))


'''lambda'''

res2 = lambda a, b: a + b
res2(5, 6)
print(res2(5, 6))

res3 = (lambda c, d: c * d)(5, 6)
print(res3)

list2 = [1, 6, 765, 54, 3, 67, 987, 3, 543, 657, 78, 99]
list3 = filter((lambda n: n > 90), list2)
print(list(list3))

'''三目运算符'''
a = 15
print('ccc') if a < 15 else print(666)

'''偏函数'''

from functools import partial
import random

l1 = [1, 34, 456, 765, 889, 8, 43, 45, 54, 765, 35, 765, 2]
l2 = [324, 4, 556, 677, 354]
l3 = [23, 44, 6, 4, 35, 667, 56, 87, 98]
new_partial=partial(filter, lambda n: n > 100)
l4=new_partial(l1)
print(list(l4))


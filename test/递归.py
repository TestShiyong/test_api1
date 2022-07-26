# def jiecheng(n):
#     if n==1:
#         return 1
#     else:
#         return n*jiecheng(n-1)
#
# print(jiecheng(5))
#
# # sum=1
# # def jiecheng(n):
# #     for i in range(1,n+1):
# #         global sum
# #         sum=sum*i
# #         print(sum)
# #
# # jiecheng(5)
#
# def jiecheng2(n):
#     if n ==1:
#         return 1
#     else:
#
#         return  n * jiecheng2(n-1)
#
#
# print(jiecheng2(5))
# '''
# 5 * n
# 4*n
# 3*n
# 2*n
# 1*n
# '''
#
#
def fbn(c):
    if c==1:
        return 1
    elif c==2:
        return 2
    else:
        return fbn(c-1)+fbn(c-2)
#
# fbn(5)

sum=1
def if_jc(n):
    global sum
    for i in range(1,n+1):
        sum*=i
    return sum

print(if_jc(5))




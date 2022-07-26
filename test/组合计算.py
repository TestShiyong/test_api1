"统计出 12345一共能组合出多少个不同的 整数"

# for i in range(1,6):
#     for j in range(1,6):
#         for k in range(1,6):
#                 if i!=j and j!=k and i!=k:
#                     print(i,j,k)


"小明有100元钱，打算买100本书，A类书籍5元一本，B类书籍3元一本，C类书籍1元两本，请用程序算出小明一共够多少种买法"

money = 100
book = 100
count = 0
for i in range(int(money / 5)):
    for j in range(int(money / 3)):
        for k in range(int(money / 0.5)):
                count += 1
print(count)

# money = 100
# book = 100
# count = 0
# for a in range(int(money/5)):
#     for b in range(int(money/3)):
#         for c in range(int(money/0.5)):
#             if a * 5 + b * 3 + c * 0.5 <= 100 and a + b + c == 100:
#                 print("a={0}, b={1}, c={2}".format(a, b, c))
#                 count += 1
# print(count)

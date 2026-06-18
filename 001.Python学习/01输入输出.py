# name = input('你的名字是：')
# age = input('你的年龄是：')
# print(f"你的名字是{name},年龄:{age}")
#
# print("你的名字是 %s,年龄是 %s" % (name, age))

# day = int(input("请输入星期几："))
# match day:
#     case 1:
#         print("周一")
#     case 2:
#         print("周二")
#     case 3:
#         print("周三")
#     case 4:
#         print("周四")
#     case 5:
#         print("周五")
#     case 6 | 7:
#         print("周末")
#     case _:
#         print("输入错误")

"""
break:终止循环
contiune:跳出这次循环，进行下一次循环

"""
# total = 0,
# i = 1
# while i <= 100:
#     if i % 2 == 0:
#         total += i
#     i = i + 1
# else:
#     print('循环结束', total)


for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{i}*{j}={i * j}", end='\t')
    print()

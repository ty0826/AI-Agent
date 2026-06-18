tuple1 = (1, 2, 3, 3, 4, 5, 6, 7, 8, 9)
"""
列表是有序，可重复，不可修改
"""
print(tuple1)
print(type(tuple1))  # <class 'tuple'>
print(tuple1[0])  # 1
print(tuple1[-1])  # 9
print(tuple1.count(3))  # 2
print(tuple1.count(10))  # 0
print(tuple1.index(3))  # 2

tuple2 = 1, 2, 3, 3, 4, 5, 6, 7, 8, 9
print(tuple2)
print(type(tuple2))  # <class 'tuple'>

a, b, c, d, *e = tuple1  # 解包：如果对应不上就用*，可以包含所有的值
print(a, b, c, d)  # 1 2 3 3
print(*e)  # 4 5 6 7 8 9

a, *b, c, d = tuple2
print(a, b, c, d)  # 1 [2, 3, 3, 4, 5, 6, 7] 8 9

a = 100
b = 200
c = 300
d = 400

d, c, b, a = a, b, c, d
"""
组包： d, c, b, a = (100,200,300,400)
解包： d=100,c=200,b=300,a=400
"""
print(a, b, c, d)

students = (
    ("S001", "王林", 85, 92, 78),
    ("S002", "李娜婧", 92, 88, 95),
    ("S003", "十三", 78, 85, 82),
    ("S004", "曾华", 88, 79, 91),
    ("S005", "周涛", 95, 96, 89),
    ("S006", "王磊", 76, 82, 77),
    ("S007", "红霞", 89, 91, 94),
    ("S008", "徐江国", 75, 69, 82),
    ("S009", "许木", 86, 89, 98),
    ("S010", "通天", 66, 59, 72)
)

# 输出每个学生的总分和和平均分
print("学号\t\t姓名\t\t语文\t\t数学\t\t英语\t\t总分\t\t平均分")
for s in students:
    total = s[2] + s[3] + s[4]
    avg = total / 3
    print(f"{s[0]}  \t  {s[1]}  \t  {s[2]}  \t  {s[3]}  \t  {total}  \t  {avg:.1f} ")

chinese_score = [s[2] for s in students]
math_score = [s[3] for s in students]
us_score = [s[4] for s in students]
print(chinese_score)  # [85, 92, 78, 88, 95, 76, 89, 75, 86, 66]
print(math_score)  # [92, 88, 85, 79, 96, 82, 91, 69, 89, 59]
print(us_score)  # [78, 95, 82, 91, 89, 77, 94, 82, 98, 72]
print(max(chinese_score), min(chinese_score), sum(chinese_score) / len(chinese_score))  # 95 66 83.0
print(max(math_score), min(math_score), sum(math_score) / len(math_score))  # 96 59 83.0
print(max(us_score), min(us_score), sum(us_score) / len(us_score))  # 98 72 85.8

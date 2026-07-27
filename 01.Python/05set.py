set = {1, 2, 3, 2, 5, 6, 7, 8, 9}
"""
列表是无序，不可重复，可修改
"""
print(set)  # {1, 2, 3, 5, 6, 7, 8, 9} 重复的直接过滤了
print(type(set))  # <class 'set'>

set.add(109)
print(set)  # {1, 2, 3, 5, 6, 7, 8, 9,109}

set.remove(109)  # 移除元素，不存在会报错
print(set)  # {1, 2, 3, 5, 6, 7, 8, 9}

set.pop()  # 随机删除
print(set)
set.clear()  # 清空
print(set)  # set()

s2 = {"apple", "banana", "cherry"}
s3 = {"apple", "banana", "cherry", "water"}
print(s2.difference(s3))  # set()
print(s3.difference(s2))  # {'water'} 找第一个参数跟第二个参数的区别，只包含在第一个集合
print(s2.union(s3))  # 并集 {"apple", "banana", "cherry", "water"}
print(s2.intersection(s3))  # 交集 {"apple", "banana", "cherry"}

# 选修足球学生名单
football_set = {"王林", "曾牛", "徐立国", "通天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}

# 选修篮球学生名单
basketball_set = {"张铁", "墨居仁", "王林", "姜老道", "曾牛", "王蝉", "韩立", "天运子", "李化元", "厉飞雨", "云露"}

# 选修法语学生名单
french_set = {"许木", "王卓", "十三", "虎咆", "姜老道", "天运子", "红蝶", "厉飞雨", "韩立", "曾牛"}

# 选修艺术学生名单
art_set = {"通天", "天运子", "韩立", "虎咆", "姜老道", "紫灵"}

# 同时选修法语和艺术的学生
fa_set2 = french_set.intersection(art_set)
fa_set2 = french_set & fa_set2
print(fa_set2)

# 同时选修了四门课程的学生
fa_set3 = french_set.intersection(art_set).intersection(basketball_set).intersection(football_set)
fa_set3 = french_set & art_set & basketball_set & football_set
print(fa_set3)

# 找出选了足球但是没有选篮球
fa_set4 = football_set.difference(basketball_set)
fa_set5 = football_set - basketball_set
fa_set6 = {s for s in football_set if s not in basketball_set}
print(fa_set4)
print(fa_set5)
print(fa_set6)

# 统计每个学生选修的课程数量
fa_set7 = french_set | art_set | basketball_set | football_set
fa_set8 = [*french_set, *art_set, *basketball_set, *football_set]
for s in fa_set7:
    print(f"{s}选修了{fa_set8.count(s)}门课程")

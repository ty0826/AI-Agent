import re

s1 = "15855195225是我的手机号，你记住了？我的另一个手机号是19956643128，另外两个QQ号是2446217554,1832141607"
s2 = "我的手机号15855195225，你记住了？我的另一个手机号是19956643128，另外两个QQ号是2446217554,1832141607"
s3 = "我的手机号15855195225; 158开头的，25结尾的;我的另一个手机号是19956643128，另外两个QQ号是2446217554,1832141607"
# match--从字符串的开头开始匹配（匹配第一项）
result = re.match(r"1[3-9]\d{9}", s1)
print(result.group())  # 15855195225
print(result.span())  # (0, 11) 获取匹配的索引
print(result.start())  # 0 获取匹配的开始索引
print(result.end())  # 11  获取匹配的最后索引

# search---从任意位置开始，搜索第一个匹配项
result = re.search(r"1[3-9]\d{9}", s2)
print(result.group())  # 15855195225
print(result.span())  # (5, 16)
print(result.start())  # 5
print(result.end())  # 16

# findall---从任意位置开始，搜索所有匹配项
result = re.findall(r"1[3-9]\d{9}", s2)
print(result)  # ['15855195225', '19956643128']

"""
 . ：字符
 *:出现任意次
 ?:最多出现一次
 +：最少出现一次
"""
result = re.findall(r"158.*", s3)  # 出现任意次
print(result)  # ['15855195225; 158开头的，25结尾的;我的另一个手机号是19956643128，另外两个QQ号是2446217554,1832141607']
result = re.findall(r"158.?", s3)  # 最多出现一次
print(result)  # ['1585', '158开']
result = re.findall(r"158.+", s3)  # 最少出现一次
print(result)  # ['15855195225; 158开头的，25结尾的;我的另一个手机号是19956643128，另外两个QQ号是2446217554,1832141607']

"""
 \d：匹配数字
 \D:匹配非数字
 \w:匹配单词字符，a-z,A-Z,0-9,_,其他语言字符
 \W：匹配非单词字符
 {m}:出现m次
 {m,}:出现m次
 {m,n}:出现m-n次
 [mn]:匹配m或者n
 [m-n]:匹配m-n的值
 [^mn]:匹配非mn
 ^:匹配字符串开头
 $:匹配字符串结尾
"""
result = re.findall(r"158\d{8}", s1)
print(result)  # ['15855195225']
result = re.findall(r"158\d{6,7}", s1)
print(result)  # ['1585519522']
result = re.findall(r"158\d{7,8}", s1)
print(result)  # ['15855195225']

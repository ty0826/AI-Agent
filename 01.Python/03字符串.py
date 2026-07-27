string = 'Python hello world'
print(type(string))  # <class 'str'>
print(string[0])  # P
print(string[-1])  # d
print(string[0:2:1])  # py
print(string[1::2])  # yhnhlowrd
print(string[1::])  # ython hello world
print(string[::2])  # Pto el ol
print(string[-1:-6:-1])  # dlrow

print(string.find('p'))  # -1 能找到就返回对应下标，找不到就返回-1
print(string.count('p'))  # 返回对应次数，区分大小写
print(string.upper())  # 大写PYTHON HELLO WORLD
print(string.lower())  # 小写python hello world
print(string.title())  # 首字母大写Python Hello World
print(string.split(" "))  # 根据分隔符分隔，转成list ['Python', 'hello', 'world']
print(string.strip("Pyld"))  # 去除字符串两端的空白字符或者指定字符 thon hello wor
print(string.replace("h", "1111"))  # 所有匹配替换指定字符1111 hello world
print(string.startswith("Python1"))  # 检查字符串是否以指定字符串开头，False
print('P' in string)  # True 判断字符串是否存在“P”

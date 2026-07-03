# 不定长参数

def calc_data(*args):
    max_data = max(args)
    min_data = min(args)
    avg_data = round(sum(args) / len(args), 1)
    return max_data, min_data, avg_data


print(calc_data(1, 2, 3))
print(calc_data(1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 0))


# 不定长参数--关键字传递
def calc_data1(*args, **kwargs):
    max_data = max(args)
    min_data = min(args)
    avg_data = sum(args) / len(args)
    # print(kwargs)  # {'round': 2, 'point': True}
    if kwargs.get('round'):
        avg_data = round(avg_data, kwargs.get('round'))
    return max_data, min_data, avg_data


print(calc_data1(1, 1, 8, round=2, point=True))

##lambda函数，匿名函数
add = lambda a, b: a + b
print(add(1, 2))  # 3

a = lambda: print('hello')
a()  # hello

data_list = ["c", "c++", "python", "javaScript", "typeScript", "java"]
data_list.sort(key=lambda item: len(item), reverse=True)
print(data_list)  # ['c', 'c++', 'java', 'python', 'javaScript', 'typeScript']


###递归函数
def fa(n):
    if n == 1:
        return 1
    else:
        return n * fa(n - 1)

sum_fa = fa(10)
print(sum_fa)
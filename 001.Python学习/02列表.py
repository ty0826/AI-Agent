list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
"""
列表是有序，可重复，可修改
"""
print(type(list))  # <class 'list'>
print(list[0], list[-1])  # A,I
print(list[0:3:1])  # [A,B,C]
print(list[:3:1])  # [A,B,C]
print(list[:-3:1])  # [A,B,C,D,E,F]
print(list[:-3])  # [A,B,C,D,E,F]

list.append(1)
print(list)  # ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 1]
list.insert(1, 2)
print(list)  # ['A', 2,'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 1]
list.remove('A')
print(list)  # [2,'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 1]
list.pop(0)
print(list)  # ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 1]
list.pop()
print(list)  # ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
list.sort()
print(list)  # ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
list.reverse()
print(list)  # ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B']

num_list = []

# for num in range(10):
#     nums = int(input(f"请输入第{num + 1}个数字："))
#     num_list.append(nums)
#
# max = max(num_list)
# min = min(num_list)
# avg = sum(num_list) / len(num_list)
# print(max, min, avg)

##列式推导
new_list1 = []
for i in range(1, 21):
    new_list1.append(i ** 2)

print(new_list1)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]
new_list2 = [i ** 2 for i in range(1, 21)]
print(new_list2)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]
new_list3 = [i ** 2 for i in range(1, 21) if i % 2 == 0]
print(new_list3)  # [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

print(''.join(map(str, [1, 2, 3, 4])))  # 1234
print(','.join(map(str, [1, 2, 3, 4])))  # 1,2,3,4
print(','.join(["a", "b", "c", "d"]))  # a,b,c,d
print('a,b,c,g'.split(','))  # ['a', 'b', 'c', 'g']
print('1,2,3,4'.split(',')) #['1', '2', '3', '4']

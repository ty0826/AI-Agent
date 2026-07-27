"""
__init__ :初始化
__str__：字符串表示方法
__eq__：比较两个对象是否相等
__lt__：小于
__le__小于等于
__gt__大于
__ge__大于等于
"""


class Car:
    def __init__(self, brand, name, price):
        self.brand = brand
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.brand} {self.name} {self.price}"

    def __eq__(self, other):
        return self.brand == other.brand and self.name == other.name and self.price == other.price

    def __lt__(self, other):
        return self.price < other.price


c1 = Car('BMW', 'X7', 50000)
print(c1)  # <__main__.Car object at 0x00000250A4F57B60>
c2 = Car('BMW', 'X7', 50000)
print(c2)  # <__main__.Car object at 0x00000250A6208A50>

print(c1 == c2) #True
print(c1 < c2) #False

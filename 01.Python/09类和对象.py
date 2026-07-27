# 定义类
class Car:
    pass


# 创建对象
c1 = Car()
c1.color = 'red'
c1.brand = 'BWM'
print(c1.__dict__)  # {'color': 'red', 'brand': 'BWM'}


class CarInfo:
    # 类属性---整个类里面都可以用的
    wheel = 4
    tax_rate = 0.1

    def __init__(self, color, brand, price):
        # 实例属性
        self.color = color
        self.brand = brand
        self.price = price

    def running(self):
        print(f"{self.color} {self.brand} 正在高速形式")

    def total_cost(self, discount: int, rate: int) -> int:
        return self.price * discount * rate


car1 = CarInfo('red', 'BWM', 10)
print(car1.__dict__)  # {'color': 'red', 'brand': 'BWM'}
car1.running()  # red BWM 正在高速形式
print(car1.total_cost(5, 10))  # 500

print(car1.color)  # red
print(car1.wheel)  # 4
# 在查找属性值时，先查找实例属性的然后再去找类属性
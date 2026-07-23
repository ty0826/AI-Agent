class Car:
    def __init__(self, brand, model, color, owner):
        self.brand = brand
        self.model = model
        self.color = color
        self.__owner = owner  # '__'私有属性

    def charge(self):
        print(f"{self.brand} {self.model} 正在补充燃料.......")


class FuelCar(Car):
    def charge(self):
        print(f"{self.brand} {self.model} 正在加油.......")


class ElectricCar(Car):
    def charge(self):
        print(f"{self.brand} {self.model} 正在充电.......")


def handle_charge(car: Car):
    car.charge()


if __name__ == "__main__":
    handle_charge(FuelCar("BMW", 'X3', "red", "张三"))  # BMW X3 正在加油.......
    handle_charge(ElectricCar("HUAWEI", 'M9', "red", "李四"))  # HUAWEI M9 正在充电.......

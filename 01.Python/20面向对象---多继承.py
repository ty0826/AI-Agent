class Car:
    def __init__(self, brand, model, color, owner):
        self.brand = brand
        self.model = model
        self.color = color
        self.__owner = owner  # '__'私有属性

    def start(self):
        print(f"{self.brand} {self.model} 正在启动.......")

    def run(self):
        print(f"{self.__owner} {self.brand} {self.model} 正在行驶......")
        self.__control_fuel()

    def stop(self):
        print(f"{self.brand} {self.model} 停止行驶......")

    def __control_fuel(self):
        print(f"{self.brand} {self.model} 正在控制油门......")

    def get_owner(self):
        return self.__owner

    def charge(self):
        print(f"{self.brand} {self.model} 正在补充燃料")


class HuaweiAIDriving:
    def __init__(self, version):
        self.version = version

    def run(self):
        print(f"使用华为智驾版本{self.version}")


class WenjieCar(Car, HuaweiAIDriving):
    def __init__(self, brand, model, color, owner, version):
        Car.__init__(self, brand, model, color, owner)
        HuaweiAIDriving.__init__(self, version)

    def run(self):
        Car.run(self)
        HuaweiAIDriving.run(self)

if __name__ == '__main__':
    car = WenjieCar("赛力斯", "M9", "red", "涛哥", '1')
    print(car.__dict__)
    car.run()
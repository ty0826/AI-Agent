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


class FuelCar(Car):
    def charge(self):
        """
            重写的两个方法:
            1、super().方法名()
            2、类名.方法名()
        """
        # super().charge() #BYD 秦plus 正在补充燃料
        Car.charge(self)  # BYD 秦plus 正在补充燃料
        print(f"{self.brand} {self.model} 正在加油")


class ElectricCar(Car):
    def charge(self):
        print(f"{self.brand} {self.model} 正在充电")


if __name__ == '__main__':
    car = Car("Audi", "A5", "red", "涛哥")
    car.start()  # Audi A5 正在启动.......
    car.run()  # Audi A5 正在行驶......
    car.stop()  # Audi A5 停止行驶......

    print(car.get_owner())  # 涛哥

    car._Car__control_fuel()
    print(car._Car__owner)  # 涛哥

    car1 = FuelCar("BYD", "秦plus", "red", "涛哥")
    car1.start()

    car2 = ElectricCar("吉利", "星元", "red", "涛哥")
    car2.start()

    car.charge()  # Audi A5 正在补充燃料
    car1.charge()  # BYD 秦plus 正在加油
    car2.charge()  # 吉利 星元 正在充电

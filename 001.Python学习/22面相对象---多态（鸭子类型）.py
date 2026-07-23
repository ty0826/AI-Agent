class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def swimming(self):
        print(f"Dog:{self.name} {self.age} 正在游泳")


class Duck:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def swimming(self):
        print(f"Duck:{self.name} {self.age} 正在游泳")


class Pig:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def swimming(self):
        print(f"Pig:{self.name} {self.age} 正在游泳")


def go_swimming(duck):
    duck.swimming()


"""
python的多态不一定非要继承父类，方法里形参不限制
"""

if __name__ == '__main__':
    go_swimming(Duck('唐老鸭', '111'))
    go_swimming(Pig('佩奇', '22'))
    go_swimming(Dog('旺财', '11'))
